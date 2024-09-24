import json
import logging
import os
import subprocess
import sys
from configparser import SafeConfigParser
from logging.config import dictConfig

from flask_cors import CORS
from flask import Flask, jsonify, stream_with_context, Response
from flask_mqtt import Mqtt, logger

app = Flask(__name__)
CORS(app)
# mqtt = Mqtt(app)
logging.basicConfig(level=logging.DEBUG)

parser = SafeConfigParser()
parser.read('config.ini')

app.config['SERVER_NAME'] = 'localhost:5150'
app.config['MQTT_BROKER_URL'] = parser.get('mqtt', 'mqtt_broker_url')
app.config['MQTT_BROKER_PORT'] = int(parser.get('mqtt', 'mqtt_broker_port'))
# app.config['MQTT_USERNAME'] = ''
# app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLIENT_ID'] = 'metadata-agents'
mqtt = Mqtt(app=app, connect_async=True, mqtt_logging=False)

agent_root_dir = parser.get('docker', 'agent_root_dir')
testbed_root_dir = parser.get('docker', 'testbed_root_dir')
app_settings_file = parser.get('docker', 'app_settings_file')
scripts_file = parser.get('docker', 'scripts_file')
server = parser.get('docker', 'server')

app_settings = open(app_settings_file)
app_settings_json = json.load(app_settings)
scripts = open(scripts_file)
scripts_json = json.load(scripts)
agent_shell_scripts = app_settings_json['AgentShellScripts']
username = app_settings_json['RegistryCredentials']['username']
password = app_settings_json['RegistryCredentials']['password']
testbed_metadata_replay = scripts_json['testbed']['testbed_metadata_replay']

default_working_directory = os.getcwd()
os.chdir('../..')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello Bitch!'


@app.route('/agents')
def agents():
    return jsonify([*agent_shell_scripts.keys()])


@app.route('/agents/<string:agent>/up', methods=['POST'])
def agentUp(agent):
    login = dockerLogin()
    cmd = agent_shell_scripts[agent]['up']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    # process_status = process.wait()
    # (output, err) = process.communicate()

    def generate():
        for line in process.stdout:
            app.logger.info(line)
            # yield line.decode('utf8').rstrip()
            mqtt.publish('metadata/agent/log', line, 2)
            yield line.decode('utf8')

    response = Response(
        stream_with_context(generate()),
        status=200,
        mimetype='text/plain'
    )
    return response


@app.route('/agents/<string:agent>/down', methods=['POST'])
def agentDown(agent):
    cmd = agent_shell_scripts[agent]['down']
    app.logger.info(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    # process_status = process.wait()
    # (output, err) = process.communicate()
    def generate():
        for line in process.stdout:
            app.logger.info(line)
            # yield line.decode('utf8').rstrip()
            mqtt.publish('metadata/agent/log', line, 2)
            yield line.decode('utf8')

    response = Response(
        stream_with_context(generate()),
        status=200,
        mimetype='text/plain'
    )
    return response


@app.route('/agents/script/up', methods=['POST'])
def agentScriptUp():
    cmd = testbed_metadata_replay['up']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    # process_status = process.wait()
    # (output, err) = process.communicate()

    def generate():
        for line in process.stdout:
            app.logger.info(line)
            # yield line.decode('utf8').rstrip()
            mqtt.publish('metadata/agent/log', line, 2)
            yield line.decode('utf8')

    response = Response(
        stream_with_context(generate()),
        status=200,
        mimetype='text/plain'
    )
    return response


@app.route('/agents/script/down', methods=['POST'])
def agentScriptDown():
    cmd = testbed_metadata_replay['down']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    # process_status = process.wait()
    # (output, err) = process.communicate()

    def generate():
        for line in process.stdout:
            app.logger.info(line)
            # yield line.decode('utf8').rstrip()
            mqtt.publish('metadata/agent/log', line, 2)
            yield line.decode('utf8')

    response = Response(
        stream_with_context(generate()),
        status=200,
        mimetype='text/plain'
    )
    return response


@app.route('/agents/ping')
def ping():
    # mqtt.publish('metadata/agents', 'pong', 2)
    # app.logger.info('pong')
    return 'pong'

@app.route('/agents/getalllogs/<string:trial_id>')
def getalllogs(trial_id):
    app.logger.info('getalllogs')
    app.logger.info(os.getcwd())
    cwd = os.getcwd()
    # os.chdir('./Tools/docker-logs')
    app.logger.info(os.getcwd())
    cmd = '{} {} {}'.format('get_all_logs.sh', '-t', trial_id)
    cmd = ['get_all_logs.sh', '-t', trial_id]
    app.logger.info(cmd)
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd='./Tools/docker-logs')

    # os.chdir(cwd)

    # out, err = p.communicate()

    # with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) as p:
    #     for line in p.stdout:
    #         mqtt.publish('metadata/agent/log', line, 2)
    #         app.logger.info(line)
    return jsonify(code=p.returncode, out=p.stdout, err=p.stderr)


def dockerLogin():
    cmd = str('docker login --username {0} --password {1} {2}'.format(username, password, server))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    (output, err) = p.communicate()
    app.logger.info('Command output : ', output)
    app.logger.info('Command exit status/return code : ', p_status)
    return output


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    app.logger.info('MQTT connecting.')
    mqtt.subscribe('trial', 2)
    app.logger.info('Subscribing to trial topic.')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    app.logger.info('on_message')
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # app.logger.info(data['payload'])
    if data['topic'].lower() == 'trial':
        trialMsg = json.loads(data['payload'])
        trial_id = trialMsg['msg']['trial_id']
        if trialMsg['msg']['sub_type'].lower() == 'stop':
            app.logger.info('trial stop detected')
            # app.logger.info(os.getcwd())
            # cmd = '{} {} {}'.format('cd ./Tools/docker-logs && get_all_logs.sh', '-t', trial_id)
            # app.logger.info(cmd)
            # with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) as p:
            #     for line in p.stdout:
            #         mqtt.publish('metadata/agent/log', line, 2)
            #         app.logger.info(line)
        elif trialMsg['msg']['sub_type'].lower() == 'start':
            app.logger.info('trial start detected')


# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     app.logger.info(buf)


if __name__ == '__main__':
    app.run(use_reloader=False)
    mqtt.init_app(app)
