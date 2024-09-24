# -*- coding: utf-8 -*-
"""
.. module:: mqtt_file_parser_test.py
   :platform: Linux, Windows, OSX
   :synopsis: Test script to determine if a file of JSON messages can be parsed

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Test script to determine if a JSON file or (directory containing JSON files)
can be parsed and converted back into JSON.  The purpose of this test script
is to identify 
"""

from MinecraftBridge.messages import (
   AgentChatIntervention,
   AgentActionPredictionMessage,
   AgentStatePredictionMessage,
   AgentFeedback,
   AgentVersionInfo,
   ASR_Message,
   BeepEvent,
   BlockageList, 
   ChatEvent,
   CompetencyTaskEvent,
   DoorEvent, 
   Experiment,
   FoVSummary, 
   FoV_BlockLocationList,
   FoV_MapMetadata,
   FoV_VersionInfo,
   FoV_Dependency,
   FoVProfile,
   FreezeBlockList,
   GasLeakPlacedEvent,
   GasLeakRemovedEvent,
   ItemDropEvent,  
   ItemEquippedEvent,
   ItemPickupEvent,
   ItemUsedEvent,  
   LeverEvent,   
   LocationEvent,  
   MarkerDestroyedEvent,  
   MarkerPlacedEvent,  
   MarkerRemovedEvent,  
   MissionStateEvent,   
   PauseEvent,
   PerturbationEvent,
   PlayerJumpedEvent,  
   PlayerSprintingEvent,  
   PlayerState,
   PlayerSwingingEvent,
   PlayerUtility,
   RoleSelectedEvent,  
   RoleText,
   RollcallRequest,
   RollcallResponse,
   RubbleCollapse,
   RubbleDestroyedEvent,  
   RubblePlacedEvent,  
   ScoreboardEvent,  
   SemanticMapInitialized, 
   Status, 
   ThreatSignList,  
   ToolDepletedEvent,  
   ToolUsedEvent,  
   TriageEvent,   
   Trial,  
   VictimsExpired,
   VictimList,   
   VictimNoLongerSafe,  
   VictimPickedUp,  
   VictimPlaced,  
   VictimsRescued,  
   VictimSignal,
   WoofEvent
)



import argparse

from MinecraftBridge.mqtt import FileBridge
from MinecraftBridge.mqtt.parsers import ParserMap


class MessageTester:
   """
   A simple class to exercise parsing and generating metadata files.  The 
   purpose is to exercise parsing and generating of all messages in a given
   metadata file.  
   """

   def __init__(self, bridge):
      """
      Arguments
      ---------
      bridge : MinecraftBridge.mqtt.FileBridge instance
      """

      self.__string_name = '[MessageTester]'

      message_classes = [ AgentChatIntervention,
                          AgentActionPredictionMessage,
                          AgentStatePredictionMessage,
                          AgentVersionInfo,
                          BeepEvent,
                          BlockageList, 
                          ChatEvent,
                          CompetencyTaskEvent,
                          DoorEvent, 
                          Experiment,
                          FoVSummary, 
                          FoV_BlockLocationList,
                          FoV_MapMetadata,
                          FoV_VersionInfo,
                          FreezeBlockList,
                          GasLeakPlacedEvent,
                          GasLeakRemovedEvent,
                          ItemDropEvent,  
                          ItemEquippedEvent,
                          ItemPickupEvent, 
                          ItemUsedEvent,  
                          LeverEvent,   
                          LocationEvent,  
                          MarkerDestroyedEvent,  
                          MarkerPlacedEvent,  
                          MarkerRemovedEvent,  
                          MissionStateEvent,   
                          PauseEvent,  
                          PlayerJumpedEvent,  
                          PlayerSprintingEvent,  
                          PlayerState,   
                          PlayerSwingingEvent,
                          RoleSelectedEvent,  
                          RubbleDestroyedEvent,  
                          RubblePlacedEvent,  
                          ScoreboardEvent,  
                          SemanticMapInitialized,  
                          ThreatSignList,  
                          ToolDepletedEvent,  
                          ToolUsedEvent,  
                          TriageEvent,   
                          Trial,  
                          VictimsExpired,  
                          VictimList,   
                          VictimNoLongerSafe,  
                          VictimPickedUp,  
                          VictimPlaced,  
                          VictimsRescued,  
                          WoofEvent ]


      self.messageProcessors = { message_class: self.handleMessage 
                                 for message_class in message_classes }

      self.bridge = bridge

      for topic in self.messageProcessors.keys():
         self.bridge.register(self, topic)


   def receive(self, message):
      """
      Callback from the bridge when a message is received

      Arguments
      ---------
      message : MinecraftBridge message instance
         Received message
      """

      processor = self.messageProcessors.get(message.__class__, None)


      # Process the message
      if processor is not None:
         try:
            processor(message)
         except Exception as e:
            print("Exception raised when processing message")
            print("Message: " + str(message))
            print("Exception: " + str(e))
      else:
         print("No message processor found for " + str(message))



   def handleMessage(self, message):
      """
      Callback for processing all received and parsed messages.  

      Arguments
      ---------
      message : MinecraftBridge message instance
         Received message to handle
      """

      # TODO: Exercise publishing to the bus
      pass



def test(input_filename, output_filename):
   """

   """

   bridge = FileBridge("Message Tester", input_filename, output_filename)

   tester = MessageTester(bridge)

   bridge.connect()

   bridge.disconnect()


def parseArguments():
   """
   Create an ArgumentParser and parse the arguments

   Return:
      An object containing the args
   """

   # Set up the parse
   parser = argparse.ArgumentParser(description='Message Tester')
   parser.add_argument('input_file', help='Input metadata file, for file replay.')
   parser.add_argument('output_file', help='Output metadata file, for file replay.')

   # Return the parsed arguments
   return parser.parse_args()


if __name__=='__main__':
   """
   """

   # Parse the command line arguments
   args = parseArguments()

   print("  Input File: ", args.input_file)

   test(args.input_file, args.output_file)

   print("  Done: ", args.input_file)


