import sys
import getpass

sys.path.append("/home/malmo/MalmoPlatform/build/install/Python_Examples/MQTTClient")

from RawConnection import RawConnection, RawMessage

import asyncio
from datetime import datetime
import json

import os
import io



p1 = RawConnection("Malmo-Container")

################################################################################
# Connection callback

def onConnection(isConnected, rc):
    print('Connected? {0} ({1})'.format(isConnected, rc))

# Message callback
def onMessage(message):
    try:              
        print(f'onMessage callback: {message}')
        # jsonDict = message.jsondata
        # messageType = jsonDict["header"]["message_type"]
        # print(f'message_type: {messageType}')
        # if( messageType == 'experiment'):            
            
    except Exception as ex:
        print(ex)
        print('RX Error, topic = {0}'.format(message.key))



# Add headers
def addHeader(jsonDict: dict):
    
    jsonDict["header"] = {}
    jsonDict["header"]["timestamp"] = str(datetime.utcnow().isoformat())+'Z'
    jsonDict["header"]["message_type"] = "status"
    jsonDict["header"]["version"] = "0.2" 
    

# Set up callbacks
p1.onConnectionStateChange = onConnection
p1.onMessage = onMessage

# Connect and subscribe to messages on a certain topic
p1.connect()
# p1.subscribe("control")
# p1.subscribe("experiment")
################################################################# 

# async heartbeat communication section
async def publishHeartbeatLoop(seconds):
  while(True):
    jsonDict = {}
    addHeader(jsonDict)
    jsonDict["msg"] = {}
    jsonDict["msg"]["state"] = "ok"
    p1.publish(RawMessage("status/malmo/heartbeats", jsondata=jsonDict))
    print(jsonDict)
    await asyncio.sleep(seconds)
    # we never return as we want this to run indefinitely
    
#################################################################

def stop(task):
    task.cancel()  


def classLoop():  
    loop = asyncio.get_event_loop()   
    task1 = loop.create_task(publishHeartbeatLoop(10))      
    loop.run_until_complete(task1)    

classLoop() 
##################################################################
