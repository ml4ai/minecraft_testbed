import json,traceback

# messages >= 90 at the end of a 15min mission (~1 every 10sec)

def ac_cornell_ta2_teamtrust_test(name,lines,table:dict):

    # output is a dict used to store your result before putting it in the table at the end of this function
    # The key is the unqiue id of the test ( agent_name_int)
    # The value is a tuple of length three [agent_name,success,extra_data,predicate]    
    
    output={}

    count = 0

    # Add any variables you need to keep track of here
    isTrainingMission = True    
    comp_messages_during_mission = 0 
    mission_running = False    

    for i in range(len(lines)):
            
        # line to json
        json_line = json.loads(lines[i])

        try: 

            # do your line by line testing here to inform any aggregate tasks later on below                 
            if ('topic' in json_line):
                topic = str(json_line['topic']).lower()
                if(topic == 'trial'):
                    if('msg' in json_line):
                        msg = json_line['msg']
                        if('sub_type' in msg):
                            sub_type = str(msg['sub_type']).lower()
                            if(sub_type == 'start'):                                
                                if('data' in json_line):
                                    data = json_line['data']
                                    if 'experiment_mission' in data:
                                        mission = str(data['experiment_mission']).lower()
                                        if mission.find("training") == -1:
                                                isTrainingMission = False
                
                elif(topic == 'observations/events/mission'):
                        if('data' in json_line):
                            data = json_line['data']
                            if 'mission_state' in data:
                                mission_state = str(data['mission_state']).lower()
                                if mission_state == "start":
                                        mission_running = True
                                elif mission_state == "stop":
                                        mission_running = False                                           
                
                elif(topic == 'agent/ac/player_compliance'):
                    if(mission_running):                        
                        comp_messages_during_mission+=1
                


        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        
        count += 1

    ######################################################################################
    # Do your testing of some aggregate value after all lines above have been processed here

    # SOME AGGREGATE TESTS HERE 

    boolean1 = False   
    
    if(isTrainingMission == False):        
        boolean1 = comp_messages_during_mission>90
    else:
        boolean1 = True
          
  

    output[name+'_'+str(len(output.items()))] = name, str(boolean1) , '# comply messages : ' + str(comp_messages_during_mission) , '# messages > 90 if trial!= training '  
   

    #######################################################################################
    # Write results to the global table that will print to a file   
    # where k is the id of the test
    # v is a tuple of length three [name,success,data,predicate] 
    # where name is the agent name, success is a boolean T/F, and data is extra data you've given to accompany the result   
    # output[agent_name_someint] = [ agent_name , str(true/False predicate) indicating success, some (short) extra string info for yourself,"#messages>7"]
    #######################################################################################
    for k, v in output.items():
        table[k]=v