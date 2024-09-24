from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
import requests
import MalmoPython
import os
import sys
import time
import io
from datetime import datetime
import json

# SETTING UP MQTT CLIENT

# this is one way for python to find the class
sys.path.append("/home/malmo/MalmoPlatform/build/install/Python_Examples/MQTTClient")

from RawConnection import *
from Connection import *

with open('/home/malmo/MalmoPlatform/build/install/Python_Examples/ConfigFolder/config.json') as config_file:
    data = json.load(config_file)

# GET EXPERIMENT ID AND ADD TO EACH OBSERVATION
resp = requests.get('http://malmocontrol:5002/api/experiment/getIds', verify=False)    
experiment_id = resp.json()["experiment_id"]
trial_id = resp.json()["trial_id"]

obCount = 0


################################################################################
# Connection callback

def onConnection(isConnected, rc):
    print('Connected? {0} ({1})'.format(isConnected, rc))

################################################################################
# Message callback
# CONNECTION
# def onMessage(message,prepend=''):
#     try:
#         # Process content
#         # if (message.contentType == "application/json"):
#         #     x = json.loads(message.payload.decode("utf-8"))
#         #     print('RX JSON {}= {}'.format(prepend,json.dumps(x, default=lambda o: o.__dict__, sort_keys=True, indent=4)))
#         # else:
#         #     print('RX Message {prepend}= {0}'.format(prepend,
#         #         "\n\t".join("{}: {}".format(k, v) for k, v in message.__dict__.items())
#         #         ))
#     except Exception as ex:
#         print(ex)
#         print('RX Error, topic = {0}'.format(message.key))

# RAW CONNECTION
# def onMessage(message):
#     try:
#         print(f'default callback: {message}')

#     except Exception as ex:
#         print(ex)
#         print('RX Error, topic = {0}'.format(message.key))

################################################################################
# Convert Malmo observations to an array of state messages
def createPlayerStateArray(observation):
    jsonList = []    
    timestamp = str(datetime.datetime.utcnow().isoformat())+'Z'

    if ('entities' not in observation or type(observation["entities"]) is not list):
        return None

    # Loop through entities
    for entity in observation["entities"]: 
        if ('life' not in entity or  type(entity["life"]) is not float):
            continue

        jsonDict = {}

        # Header
        jsonDict["header"] = {}
        header = jsonDict["header"]
        header["timestamp"] = timestamp
        header["message_type"] = "observation"
        header["version"] = "0.3"
        
        # Message
        jsonDict["msg"] = {}
        msg = jsonDict["msg"]
        msg["experiment_id"] = experiment_id
        msg["trial_id"] = trial_id
        msg["timestamp"] = timestamp
        msg["source"] = "simulator"
        msg["sub_type"] = "state"
        msg["version"] = "0.3"

        # Data
        jsonDict["data"] = {}
        data = jsonDict["data"]
        data["timestamp"] = timestamp
        data["observation_number"] = obCount
        data["name"] = entity["name"]
        data["world_time"] = observation["WorldTime"]
        data["total_time"] = observation["TotalTime"]
        data["entity_type"] = "human"
        data["yaw"] = entity["yaw"]
        data["x"] = entity["x"]
        data["y"] = entity["y"]
        data["z"] = entity["z"]
        data["pitch"] = entity["pitch"]
        data["id"] = entity["id"]
        data["motion_x"] = entity["motionX"]
        data["motion_y"] = entity["motionY"]
        data["motion_z"] = entity["motionZ"]
        data["life"] = entity["life"]
    
        jsonList.append(jsonDict)

    return jsonList

################################################################################
# Example pub/sub client loop

# Connection
#p1 = Connection(RawConnection("Malmo-Server"))
# RawConnection
p1 = RawConnection("Malmo-Server")


# Set up callbacks
p1.onConnectionStateChange = onConnection
#p1.onMessage = onMessage

# Connect and subscribe to messages
p1.connect()
p1.subscribe("#")

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>

            <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>12000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                  </Time>
                  <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FileWorldGenerator src="/home/malmo/MalmoPlatform/build/install/Python_Examples/Sparky"/>
                    <ServerQuitFromTimeUp timeLimitMs="'''+str(data['missionTime'])+'''"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
            </ServerSection>

              <AgentSection mode="Survival">
                <Name>Agent Ed</Name>
                <AgentStart>
                  <Placement x="-2185" y="52" z="177"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ObservationFromNearbyEntities>
                        <Range name="entities" xrange="'''+str(data['observeX'])+'''" yrange="'''+str(data['observeY'])+'''" zrange="'''+str(data['observeZ'])+'''" />
                    </ObservationFromNearbyEntities>                  
                  <ObservationFromChat/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')


# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")     
    time.sleep(float(data['observationInterval']))        
    world_state = agent_host.peekWorldState()   
    #Message --> for PMEngine with wrapper
    #p1.publish(Message("malmo/test/"+str(instance),jsondata=dict(observationNumber="#" + str(count), timestamp= str(datetime.datetime.now()), observation=json.loads(world_state.observations[0].text) )))
    #RawMessage --> Raw JSON if needed
    if(len(world_state.observations)>0):
        obCount = obCount+1
        jsonArray = createPlayerStateArray(observation=json.loads(world_state.observations[0].text))
        if (jsonArray is not None):
            for message in jsonArray: 
                p1.publish(Message("observations/state",jsondata=message))
                
       
    for error in world_state.errors:
        print("Error:",error.text)
print()
print("Mission ended")
# Mission has ended.
