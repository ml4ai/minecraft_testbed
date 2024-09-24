#!/usr/bin/env python3
#
# Copyright (c) 2020 SIFT
#
"""
Script to launch just the testbed components we need.
"""

import argparse
from datetime import datetime
import json
import sys
import _thread
import threading
import time
import uuid

from getkey import getkey
import mcrcon
import paho.mqtt.client as mqtt

def main(args):
    """Main entry point for script."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('player_name',
                        help='The name of the Minecraft player to allow.')
    config = parser.parse_args(args)

    config.mqtt_host = 'localhost'
    # config.player_name = 'Player212'

    client = mqtt.Client(userdata=config)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Blocking connect.
    connect_to_mqtt(client, config)

    setup_keyboard_handling(client, config)

    print('Starting MQTT message loop')
    client.loop_forever()


def setup_keyboard_handling(client, config):
    """
    Sets up a background thread monitoring stdin for keypresses and acting
    accordingly.
    """
    # See: https://pypi.org/project/getkey/
    print('Setting up keyboard handling')
    thread = threading.Thread(target=handle_keypresses, args=(client, config,))
    thread.daemon = True
    thread.start()


def handle_keypresses(client, config):
    """
    Reads and responds to key presses.
    """
    done = False
    while not done:
        print_key_prompt()
        what = getkey()
        # print(f'what? "{what}"')
        if what == 's':
            print('Sending start trial message')
            send_trial_start(client, config)

        elif what == 'r':
            print('Sending rollcall request')
            send_rollcall_request(client, config)

        elif what == 'q':
            done = True

    print('Done, exiting')
    _thread.interrupt_main()


def print_key_prompt():
    """
    Print the prompt for key presses.
    """
    print('Waiting for a keypress.')
    print('  s   -   start trial message')
    print('  r   -   rollcall message')
    print('  q   -   quit')


def connect_to_mqtt(client, config):
    """
    This is a blocking call to connect to the MQTT. If the MQTT is not running,
    this will loop, repeatedly trying to connect until successful. We limit this
    loop to a slow retry (once per second).
    """
    mqtt_port = 1883
    print(f'Connecting to MQTT at: {config.mqtt_host}:{mqtt_port}')

    # If the MQTT is not running, the connect call will fail with a
    # ConnectionRefusedError. So, we try repeatedly until we succeed.
    connected = False
    start_time = time.perf_counter()
    failed_count = 0
    while not connected:
        try:
            client.connect(config.mqtt_host, mqtt_port, 60)
            connected = True
        except ConnectionRefusedError:
            # Connection attempt failed, wait a short time and try again.
            if failed_count == 0:
                print('MQTT is not running, will keep trying.')
            failed_count += 1

            # Sleep a bit before we try again.
            time.sleep(1.0)

    if failed_count == 0:
        print('Successfully connected on first try')
    else:
        end_time = time.perf_counter()
        duration_s = end_time - start_time
        print(f'Successfully connected after {duration_s:.2f} seconds ' +
              f'and {failed_count + 1} attempts')


def on_connect(client, _userdata, _flags, _rc):
    """
    Subscribe to the desired messages whenever we connct.
    """
    client.subscribe('control/#')


def on_disconnect(client, config, _rc):
    """
    When we disconnect, wait around to reconnect.
    """
    print('Lost connection to MQTT.')
    connect_to_mqtt(client, config)


# Watching the MQTT bus, this is the message sent by the MalmoControl GUI.
#
# b'{\n  "experiment_id": "afab7484-2170-472a-96b4-5c030efff31e",\n  "trial_id":
# "d9e3e281-ea92-4fb1-9183-3e97faae1e74",\n  "mission_name": "Saturn_A",\n
# "map_name": "Saturn_1.6_3D",\n  "map_block_filename":
# "MapBlocks_SaturnA_1.5_xyz.csv",\n  "map_info_filename": "",\n
# "observer_info": [],\n  "callsigns": {\n    "": "Player212"\n  },\n
# "participant_ids": {\n    "Player212": ""\n  }\n}'
#
# And to remove the initial blocking wall. Found this in
# eventmanagers/PlayerInteractionEventHandler.java.
#
# "fill -2153 60 110 -2155 62 110 minecraft:air"
#
# We found RCON information in: MinecraftServer/data/server.properties. And
# found same information in docker-compose.minecraft.yml .
#
# RCON port:      25575
# RCON password:  minecraft
#
def on_message(client, userdata, message):
    """
    Handle messages on topics we subscribed to.
    """
    print('Got MQTT message for topic: ' + message.topic)
    # print(message.payload)
    if message.topic == 'control/request/getTrialInfo':
        print('Got trial info request from Minecraft server')

        # See mcrcon usage information here:
        # https://pypi.org/project/mcrcon/
        print('Using RCON to remove the initial blocking wall.')
        with mcrcon.MCRcon('localhost', 'minecraft', port=25575) as mcr:
            print('  connected to RCON')
            print('  removing wall')
            resp = mcr.command('fill -2153 60 110 -2155 62 110 minecraft:air')
            print(f'  response: {resp}')

            print('  adding mission block')
            resp = mcr.command('fill -2153 60 121 -2153 60 121 asistmod:block_mission_mission')
            print(f'  response: {resp}')

        send_client_info(client, userdata)

        # We were sending these automatically. Now we expose them via keypresses
        # in the console. Still, we might consider bringing this back to reduce
        # interaction.
        #
        # send_trial_start(client, userdata)
        # send_rollcall_request(client, userdata)

        return

    print(message.payload)


def send_client_info(client, userdata):
    """
    Sends the client info response so that Minecraft will let the player join.
    """
    # See: MalmoControl/MQTTProcessor.cs
    # And note that some of these values come from:
    # testbed/Local/MalmoControl/appsettings.Production.json
    #
    trial_info = {
        'experiment_id': 'null-experiment',
        'trial_id': 'null-trial',
        'mission_name': 'Saturn_A',
        'map_name': 'Saturn_2.0_3D',
        'map_block_filename': 'MapBlocks_SaturnA_2.0_xyz.csv',
        'map_info_filename': None,
        'observer_info': [],
        'callsigns': {
            userdata.player_name: 'Red'
            # 'Green': [],
            # 'Blue': []
        },
        'participant_ids': []
    }
    print('Sending trial info')
    client.publish('control/response/getTrialInfo', json.dumps(trial_info))


def send_trial_start(client, userdata):
    """
    Sends the trial start message so that a whole bunch of things will work.
    """
    print('Sending trial start')
    # See:
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Trial/trial.md
    data = {
        'client_info': [
            {
                'playername': userdata.player_name,
                # 'callsign': 'Alpha',
                'participantid': 'p1'
            }
        ]
    }
    message = make_common_message('trial', 'start', data, userdata)
    client.publish('trial', json.dumps(message))


def send_rollcall_request(client, userdata):
    """
    Sends a rollcall request so we can see if clients are behaving themselves.
    """
    print('Sending rollcall request')
    # See:
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/rollcall/agent_rollcall.md
    data = {
        'rollcall_id': str(uuid.uuid4())
    }
    message = make_common_message('agent', 'rollcall:request',
                                  data, userdata)
    client.publish('agent/control/rollcall/request', json.dumps(message))


def make_common_message(msg_type, msg_subtype, data, userdata):
    """
    Prepares and returns a message object with the required header, msg, and
    data fields.
    """
    # See:
    # https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Common_Header/common_header.md
    header = {
        'timestamp': generate_timestamp(),
        'message_type': msg_type,
        'version': '0.1'
    }
    msg = {
        'experiment_id': 'null-experiment',
        'trial_id': 'null-trial',
        'timestamp': generate_timestamp(),
        'source': 'bootstrap',
        'sub_type': msg_subtype,
        'version': '0.1'
    }
    return {
        'header': header,
        'msg': msg,
        'data': data
    }


def generate_timestamp():
    """
    Makes an ASIST-happy timestamp. Copied from:
    https://gitlab.com/ihmc-asist/python-agent-helper/-/blob/main/src/asistagenthelper/ASISTAgentHelper.py#L157
    """
    return str(datetime.utcnow().isoformat()) + 'Z'


# ------------------------------------------------------------
# This is the magic that runs the main function when this is invoked
# as a script.

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
