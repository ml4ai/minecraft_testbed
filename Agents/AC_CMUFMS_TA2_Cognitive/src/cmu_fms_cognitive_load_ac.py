"""
CMU FMS Cognitive Load Analytic Component
"""

import json
import logging
import math
import os
import uuid

from pprint import pprint       # only used for testing and debugging

import pyactup

from asistagenthelper import ASISTAgentHelper

# if non-empty INSTRUMENTATION should be a directory path into which to scribble
INSTRUMENTATION = os.environ.get("ASIST_COGNITIVE_INSTRUMENTATION")
instrumentation_file = None

# Cognitive parameters
NOISE = 0.0
DECAY = 0.5
TEMPERATURE = 1
THRESHOLD = -1.0

CONFIDENCE_OFFSET = 0.25


class CMUFMSCognitiveLoadAC:

    def __init__(self):
        self.helper = ASISTAgentHelper(self.on_message)
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s"))
        self.helper.get_logger().setLevel(logging.INFO)
        self.helper.get_logger().addHandler(log_handler)
        self.logger = logging.getLogger(self.helper.agent_name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(log_handler)
        extra_path = os.path.join(self.helper.config_folder, "extraInfo.json")
        self.extra_info = {}
        if os.path.exists(extra_path):
            with open(extra_path) as extra_file:
                self.extra_info = json.load(extra_file)
        if "default" not in self.extra_info.keys():
            self.extra_info["default"] = "I guess {0} is an okay role."
        self.memory = pyactup.Memory(noise=NOISE,
                                     decay=DECAY,
                                     temperature=TEMPERATURE,
                                     threshold=THRESHOLD,
                                     learning_time_increment=0)
        self.reset()

    def reset(self):
        self.memory.reset()
        self.last_elapsed_milliseconds = 0
        self.last_milliseconds_emitted = 0
        self.victims_seen = dict()
        self.victims_evacuated = set()

    def start(self):
        self.helper.set_agent_status(self.helper.STATUS_UP)
        self.logger.info("Starting Agent Loop on a separate thread.")
        self.helper.start_agent_loop_thread()
        self.logger.info("Agent is now running...")

    def on_message(self, topic, header, msg, data, mqtt_message):
        global instrumentation_file
        self.logger.debug(f"{topic} message received")
        self.logger.debug(f"{data}")
        if topic == "trial":
            subtype = msg.get("sub_type")
            if subtype == "start":
                self.reset()
                name = data.get('name')
                self.logger.info(f"starting trial {name}")
                if INSTRUMENTATION:
                    # Note that this instrumentation stuff works only in Unix
                    instrumentation_file = f"{INSTRUMENTATION}/{name}.json"
                    with open(instrumentation_file, "w") as f:
                        pass    # create an empty file
            elif subtype == "stop":
                self.logger.info("finished trial")
                if INSTRUMENTATION:
                    # skip the near interminable pointless noise following the actual trial
                    os.system("pkill -f MQTTPlayback")
            else:
                self.logger.warning(f"unexpected trial message received {subtype}")
            return
        elapsed = data.get("elapsed_milliseconds")
        if elapsed is None:
            elapsed = data.get("jag")
            if elapsed is not None:
                elapsed = elapsed.get("elapsed_milliseconds")
        if elapsed is not None:
            self.last_elapsed_milliseconds = max(elapsed, self.last_elapsed_milliseconds)
        seconds = self.last_elapsed_milliseconds / 1000
        if seconds < self.memory.time:
            self.helper.logger.warning("time appears to be running backward")
            seconds = self.memory.time
            self.last_elapsed_milliseconds = ceil(seconds * 1000)
        self.memory._time = seconds
        if topic == "observations/events/player/jag":
            if (msg["sub_type"] == "Event:Discovered"
                  and "jag" in data.keys()
                  and "inputs" in data["jag"]
                  and "victim-id" in data["jag"]["inputs"]):
                self.logger.debug(f"jag victim-id: {data['jag']['inputs']['victim-id']}")
                victim = data["jag"]["inputs"]["victim-id"]
                try:
                    if victim <= 0:
                        self.logger.warning(f"non-positive victim ID {victim}")
                        return
                except TypeError:
                    self.logger.warning(f"non-numeric victim ID {victim}")
                    return
                if victim in self.victims_evacuated:
                    return
                if victim in self.victims_seen:
                    self.victims_seen[victim] += 1
                    n = self.victims_seen[victim]
                    if n > 3:
                        self.logger.warning(f"victim {victim} discovered for the {n}th time")
                else:
                    self.logger.debug(f"victim {victim} seen")
                    self.victims_seen[victim] = 1
                self.memory.learn(victim_id=victim)
            else:
                return
        elif topic == "observations/events/server/victim_evacuated" and data["success"]:
            victim = data["victim_id"]
            if victim not in self.victims_seen:
                self.logger.warning(f"evacuating an undiscovered victim {victim}")
            if victim in self.victims_evacuated:
                self.logger.warning(f"victim already evacuated {victim}")
                return
            self.victims_evacuated.add(victim)
        elif topic in ("observations/events/player/victim_placed",
                       "observations/events/player/triage",
                       "observations/events/server/victim_evacuated"):
            victim = data["victim_id"]
            if victim not in self.victims_seen:
                self.logger.warning(f"interacting with an undiscovered victim {victim} "
                                    f"({topic[topic.rindex('/')+1:]})")
            if victim in self.victims_evacuated:
                return
            self.memory.learn(victim_id=victim)
        else:
            self.logger.warning(f"Unexpected {topic} message recieved: {data}")
            return
        with self.memory.current_time:
            self.memory.advance()
            activations = [ a for a in [ (c._activation(), 1 + math.log(c._reference_count))
                                         for c in self.memory.values()
                                         if c["victim_id"] not in self.victims_evacuated ]
                            if a[0] >= self.memory.threshold ]
        mid = self.exponentials(activations)
        low = self.exponentials(activations, CONFIDENCE_OFFSET)
        high = self.exponentials(activations, -CONFIDENCE_OFFSET)
        load = cognitive_load(mid)
        forgetting = probability_of_forgetting(mid)
        response_data = {
            "id": str(uuid.uuid4()),
            "agent": self.helper.agent_name,
            "created": self.helper.generate_timestamp(),
            "elapsed_milliseconds": self.last_elapsed_milliseconds,
            "cognitive_load": {
                "value": load,
                "confidence": confidence(cognitive_load(low),
                                         load,
                                         cognitive_load(high)) },
            "probability_of_forgetting": {
                "value": forgetting,
                "confidence": confidence(probability_of_forgetting(low),
                                         forgetting,
                                         probability_of_forgetting(high)) }}
        self.logger.debug(f"sending cognitive agent information: {json.dumps(response_data)}")
        self.helper.send_msg(f"agent/measure/{self.helper.agent_name}/load",
                             "agent",
                             "Measure:cognitive_load",
                             "1.0",
                             timestamp=msg["timestamp"],
                             data=response_data)
        if INSTRUMENTATION:
            del response_data["id"], response_data["agent"], response_data["created"]
            response_data["action"] = ("victim_discovered" if topic == "observations/events/player/jag"
                                       else topic[topic.rindex("/")+1:])
            with self.memory.current_time:
                self.memory.advance()
                for c in self.memory.values():
                    id = c["victim_id"]
                    if id not in self.victims_evacuated:
                        a = c._activation()
                        if a >= self.memory.threshold:
                            response_data[id] = (1 - 1 / (1 + math.exp((self.memory.threshold - a)
                                                                       / self.memory._temperature)))
            with open(instrumentation_file, "a") as f:
                jsn = json.dumps(response_data)
                print(jsn, file=f)
                print(jsn)

    def exponentials(self, activations, offset=0):
        return [ math.exp((self.memory.threshold - (a[0] + offset / a[1])) / self.memory._temperature)
                 for a in activations ]


def cognitive_load(exponentials):
    return sum(exponentials)

def probability_of_forgetting(exponentials):
    return 1 - math.prod(1 / (1 + e) for e in exponentials)

def confidence(low, middle, high):
    if middle < 0:
        self.logger.warning(f"unexpected negative measure {middle}")
        return 0
    if high >= low:
        diff = high - low
    else:
        self.logger.warning(f"mis-ordered confidence interval ({low}, {high})")
        diff = low - high
    try:
        return math.exp(-diff / middle)
    except ZeroDivisionError:
        return 1


if __name__ == "__main__":
    CMUFMSCognitiveLoadAC().start()
