import json,traceback

# number of messages = 1 during planning session per trial
def atomic_agent_test(name,lines,table:dict):    

    output={}

    count = 0

    isTrainingMission = True
    planning_session_over = False
    num_atomic_chats = 0
    num_planning_chats = 0
    
    for i in range(len(lines)):
            
        # line to json
        json_line = json.loads(lines[i])

        try:                  
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
                
                elif( topic == 'observations/events/mission/planning'):
                    if ( 'state' in data):
                        state = str(data['state']).lower()
                        if (state == 'stop'):
                            planning_session_over = True                
                elif( topic == 'agent/intervention/atomic_agent/chat'):
                    if ( planning_session_over == False ):
                        num_atomic_chats+=1
                    else:
                        num_atomic_chats+=1
                        num_planning_chats+=1


        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        
        count += 1

    boolean1 = False   
    if (isTrainingMission == False):
        if(num_planning_chats==1):
            boolean1 = True
    else:
        boolean1 = True

    output[name+'_'+str(len(output.items()))] = name, str(boolean1) , 'planning_chats,total_chats : ' + str(num_planning_chats) +','+str(num_atomic_chats),"number of messages = 1 during planning session per trial"   

    
    #######################################################################################
    # Write results to the global table that will print to a file   
    # where k is the id of the test
    # v is a tuple of length three [name,success,data,predicate] 
    # where name is the agent name, success is a boolean T/F, and data is extra data you've given to accompany the result   
    # output[agent_name_someint] = [ agent_name , str(true/False predicate) indicating success, some (short) extra string info for yourself,"#messages>7"]
    #######################################################################################   
    for k, v in output.items():
        table[k]=v