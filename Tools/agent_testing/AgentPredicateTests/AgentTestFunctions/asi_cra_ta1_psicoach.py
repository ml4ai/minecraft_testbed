
import json,traceback

# messages > 0 within 5 seconds of mission start

def asi_cra_ta1_psicoach_test(name,lines,table:dict):

    # output is a dict used to store your result before putting it in the table at the end of this function
    # The key is the unqiue id of the test ( agent_name_int)
    # The value is a tuple of length three [agent_name,success,extra_data,predicate]    
    
    output={}

    count = 0

    # Add any variables you need to keep track of here  
    isTrainingMission = True  
    mission_started = False
    num_chat_messages = 0
    num_chat_messages_5_seconds = 0
    five_seconds_in_milliseconds:int = (1000*5)
    elapsed_milliseconds:int = 0

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
                                    mission_started = True

                elif(mission_started == True):
                    if( topic == 'observations/state'):
                        if('data' in json_line):
                                data = json_line['data']
                                if 'elapsed_milliseconds' in data:
                                    elapsed_milliseconds = int(data['elapsed_milliseconds'])
                    if( topic == 'agent/intervention/asi_cra_ta1_psicoach/chat'):
                        if(elapsed_milliseconds<=five_seconds_in_milliseconds):
                            num_chat_messages_5_seconds+=1                                
                        num_chat_messages+=1

        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        
        count += 1

    ######################################################################################
    # Do your testing of some aggregate value after all lines above have been processed here    

    # SOME AGGREGATE TESTS HERE

    boolean1 = False   
    if (isTrainingMission == False):
        if(num_chat_messages>0):
            boolean1 = True
    else:
        boolean1 = True

    boolean2 = False 
    if (isTrainingMission == False):
        if(num_chat_messages_5_seconds>0):
            boolean2 = True  
    else:
        boolean2 = True

    output[name+'_'+str(len(output.items()))] = name, str(boolean1) , '# chats in mission : ' + str(num_chat_messages),"messages > 0 if not Training" 
    output[name+'_'+str(len(output.items()))] = name, str(boolean2) , '# chats within 5 : ' + str(num_chat_messages_5_seconds),"messages > 0 within 5 sec of mission start if not Training"    

    #######################################################################################
    # Write results to the global table that will print to a file   
    # where k is the id of the test
    # v is a tuple of length three [name,success,data,predicate] 
    # where name is the agent name, success is a boolean T/F, and data is extra data you've given to accompany the result   
    # output[agent_name_someint] = [ agent_name , str(true/False predicate) indicating success, some (short) extra string info for yourself,"#messages>7"]
    #######################################################################################
    for k, v in output.items():
        table[k]=v