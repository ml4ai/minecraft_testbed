#!/usr/bin/env python3

"""
ASISTAgentHelper Class

Author: Roger Carff
email:rcarff@ihmc.us
"""

import os
import time
import json
import uuid
from datetime import datetime
from helpers.RawConnection import RawConnection, RawMessage

__author__ = 'rcarff'


class ASISTAgentHelper(object):
    def __init__(self, on_message_handler):
        self.agent_name = os.getenv('AGENT_NAME', 'ASIST_Test_Agent')

        # load the preferences from the config file
        self.preferences = {}
        self.version = {}
        config_folder = 'ConfigFolder'
        if not os.path.exists(config_folder):
            config_folder = '../ConfigFolder'
        if os.path.exists(config_folder):
            with open(config_folder + '/config.json') as config_file:
                data = json.load(config_file)
                self.version = data['version_info']
                if "preferences" in data.keys():
                    self.preferences = data["preferences"]
                if "version_info" in data.keys():
                    self.version = data["version_info"]
        self.preferences['config_folder'] = config_folder
        self.preferences['agent_name'] = self.agent_name

        # start the MQTT bus pub/sub system
        print("Starting the MQTT Bus pub/sub system...")
        self.connected_to_mqtt = False
        self.trial_infos = {}
        self.message_bus = RawConnection(self.agent_name+":"+str(uuid.uuid4()))
        self.message_bus.onConnectionStateChange = self.on_connection
        self.message_bus.onMessage = self.on_message
        self.on_message_handler = on_message_handler
        self.tried_to_connect = False

    # Returns the preferences dictionary read in from the config file
    def get_preferences(self):
        return self.preferences

    # Subscribe to a topic
    def subscribe(self, topic):
        if "subscribe_topic_list" not in self.preferences.keys():
            self.preferences['subscribe_topic_list'] = []
        if topic not in self.preferences['subscribe_topic_list']:
            self.preferences['subscribe_topic_list'].append(topic)
            if self.connected_to_mqtt:
                self.message_bus.subscribe(topic)

    # Unsubscribe to a topic
    def unsubscribe(self, topic):
        if "subscribe_topic_list" not in self.preferences.keys():
            return
        if topic in self.preferences['subscribe_topic_list']:
            self.preferences['subscribe_topic_list'].remove(topic)
            if self.connected_to_mqtt:
                self.message_bus.unsubscribe(topic)

    # returns an ASIST happy timestamp string for the current date and time
    def generate_timestamp(self):
        return str(datetime.utcnow().isoformat()) + 'Z'

    # Publish an ASIST message to the message bus with the given info and at the current system time.
    # - trial_info is expected to be a dict with values for experiment_id and trial_id and optionally
    #   replay_id and replay_root_id.
    def send_msg(self, topic, message_type, sub_type, msg_version, trial_info, data):
        timestamp = self.generate_timestamp()
        self.send_msg_with_timestamp(topic, message_type, sub_type, msg_version, trial_info, timestamp, data)

    # Publish an ASIST message to the message bus with the given info and timestamp
    # - trial_info is expected to be a dict with values for experiment_id and trial_id and optionally
    #   replay_id and replay_root_id.
    def send_msg_with_timestamp(self, topic, message_type, sub_type, msg_version, trial_info, timestamp, data):
        json_dict = {}
        json_dict["header"] = {}
        json_dict["header"]["timestamp"] = timestamp
        json_dict["header"]["version"] = "1.1"
        json_dict["header"]["message_type"] = message_type

        json_dict["msg"] = {}
        json_dict["msg"]["sub_type"] = sub_type
        json_dict["msg"]["timestamp"] = timestamp
        json_dict["msg"]["experiment_id"] = trial_info['experiment_id']
        json_dict["msg"]["trial_id"] = trial_info['trial_id']
        if trial_info['replay_root_id'] is not None:
            json_dict["msg"]["replay_root_id"] = trial_info['replay_root_id']
        if trial_info['replay_id'] is not None:
            json_dict["msg"]["replay_id"] = trial_info['replay_id']
        json_dict["msg"]["version"] = msg_version
        json_dict["msg"]["source"] = self.agent_name

        if data is not None:
            json_dict["data"] = data

        self.message_bus.publish(RawMessage(topic, jsondata=json_dict))

    # Returns the MQTT bus connection state.
    def is_connected(self):
        return self.connected_to_mqtt

    # This method reconnects to the message bus if disconnected.
    # It should be called routinely by anyone using this helper class
    def check_and_reconnect_if_needed(self):
        if not self.connected_to_mqtt:
            try:
                self.message_bus.connect()
            except Exception as ex:
                if not self.tried_to_connect:
                    print("- Failed to connect, MQTT Message Bus is not running!!")
                    self.tried_to_connect = True
        else:
            self.tried_to_connect = False

        time.sleep(0.1)
        return None

    # MQTT Connection callback
    #   Called when connected to or disconnected from the MQTT Message bus
    def on_connection(self, is_connected, rc):
        if self.connected_to_mqtt == is_connected:
            return

        self.connected_to_mqtt = is_connected
        if self.connected_to_mqtt:
            print('- Connected to the Message Bus.')
            if "subscribe_topic_list" in self.preferences.keys():
                for topic in self.preferences["subscribe_topic_list"]:
                    self.message_bus.subscribe(topic)
                    print('- subscribed to topic: ' + topic)
        else:
            print('- Disconnected from the Message Bus!!')

    # MQTT Message callback
    #  Called when there is a message on the message bus for a topic which we are subscribed to
    def on_message(self, message):
        try:
            topic = message.key
            if topic != 'observations/state' and topic != 'observations/events/player/location':
                print("AG::on_message: received msgs with topic: " + topic)
            json_dict = message.jsondata
            self.on_message_handler({"topic": topic, "message": json_dict})

        except Exception as ex:
            print(ex)
            print('RX Error, topic = {0}'.format(message.key))
