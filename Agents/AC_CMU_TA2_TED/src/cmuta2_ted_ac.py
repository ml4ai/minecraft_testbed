#!/usr/bin/env python3

"""
CMU TA2 Diagnostic AC

Author: Jeff Rye
email: rye@sift.net

This is a real-time/online implementation of CMU's diagnostic agent. Jeff used
the IHMC started agent as a base and translated CMU's algorithms and code to
operate on a live message stream.
"""

import argparse
import logging
import os
import sys
import traceback

import json5 as json

from asistagenthelper import ASISTAgentHelper

import computations

__author__ = 'jrye'


def main(args):
    """Main entry point for script."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plot-coverage',
                        dest='plot_coverage',
                        action='store_true',
                        help='If set, will write a series of png files ' +
                        'showing the visited positions that drive the ' +
                        'coverage metric.')
    config = parser.parse_args(args)
    config.unrecognized_topics = set()

    config.results_dir = os.path.join(os.path.dirname(__file__), '../results')
    os.makedirs(config.results_dir, exist_ok=True)

    setup_helper(config, on_message)
    setup_logging(config)

    # Load additional configuration information.
    load_extra_info(config)

    # Initialize our score tracking.
    computations.initialize_state(config)

    # examples of manually subscribing and unsubscribing to topics
    # config.helper.subscribe('observations/events/player/tool_used')
    # config.helper.unsubscribe('observations/events/player/triage', 'event', 'Event:Triage')

    # Set the agents status to 'up' and start the agent loop on a separate
    # thread
    config.helper.set_agent_status(config.helper.STATUS_UP)
    config.logger.info("Starting Agent Loop on a separate thread.")
    config.helper.start_agent_loop_thread()
    config.logger.info("Agent is now running...")

    # if you need to do anything else you can do it here and if you want to stop
    # the agent thread you can run the following, but until the agent loop is
    # stopped, the process will continue to run.
    #
    # helper.stop_agent_loop_thread()


def setup_helper(config, on_message_func):
    """
    Create the ASIST helper instance. Store it on the config.
    """
    def internal_on_message(topic, _header, msg, data, mqtt_message):
        try:
            on_message_func(topic, msg, data, mqtt_message, config)
        except Exception as ex:
            print('Exception in on_message handler')
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            raise ex

    # Agent Initialization
    config.helper = ASISTAgentHelper(internal_on_message)


def setup_logging(config):
    """
    Setup the logging for the helper and this agent.
    """
    # Set the helper's logging level to INFO.
    log_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s")
    log_handler.setFormatter(formatter)
    config.helper.get_logger().setLevel(logging.INFO)
    config.helper.get_logger().addHandler(log_handler)

    # Create our own logger.
    config.logger = logging.getLogger(config.helper.agent_name)
    config.logger.setLevel(logging.INFO)
    config.logger.addHandler(log_handler)


def load_extra_info(config):
    """
    Load extra info from the ConfigFolder for use later.
    """
    extra_path = os.path.join(config.helper.config_folder, 'extraInfo.json')
    config.extra_info = {}
    if os.path.exists(extra_path):
        with open(extra_path, encoding='utf-8') as extra_file:
            config.extra_info = json.load(extra_file)

    print(f'Loaded: {extra_path}')
    # period_ms = config.extra_info['period_ms']
    # print(f'  Update period:   {period_ms} ms')
    for key, val in config.extra_info.items():
        print(f'  {key:25}  {val}')


# This is the function which is called when a message is received for a topic
# which this Agent is subscribed to.
def on_message(topic, msg, data, _mqtt_message, config):
    """
    Handles a single message from the MQTT bus.
    """
    # config.logger.info("Received a message on the topic: " + topic)
    # if 'topic' not in mqtt_message:
    #     mqtt_message['topic'] = topic

    computations.check_elapsed_time(data, config)

    # Now handle the message based on the topic.  Refer to Message Specs for the
    # contents of header, msg, and data
    if topic == 'trial':
        config.logger.info(" - Trial Event: " + msg['sub_type'])
        # Reset the tracking values.
        computations.initialize_state(config)
        computations.record_aliases(data, config)
        return

    if topic == 'observations/events/mission':
        mission_state = data['mission_state']
        config.logger.info(f" - Mission Event: {mission_state}")
        if mission_state.lower() == 'start':
            computations.mission_start(data, config)
        else:
            computations.mission_stop(data, config)
        return

    # Now record any relevant data for later scoring.
    computations.process_message(topic, data, config)


# ------------------------------------------------------------
# This is the magic that runs the main function when this is invoked
# as a script.

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
