
import json,traceback

# # messages > 0 within 2.5 minutes of mission start if trial != Training

def ac_gallup_ta2_gold_test(name,lines,table:dict):

    # output is a dict used to store your result before putting it in the table at the end of this function
    # The key is the unqiue id of the test ( agent_name_int)
    # The value is a tuple of length three [agent_name,success,extra_data,predicate]    
    
    output={}

    count = 0

    # Add any variables you need to keep track of here
    
     
    elapsed_milliseconds = 0
    num_gold_messages = 0
    mission_running = False

    for i in range(len(lines)):
            
        # line to json
        json_line = json.loads(lines[i])

        try: 

            # do your line by line testing here to inform any aggregate tasks later on below                 
            if ('topic' in json_line):
                topic = str(json_line['topic']).lower()           
               
                if(topic == 'observations/events/mission'):
                    if('data' in json_line):
                        data = json_line['data']
                        if 'mission_state' in data:
                            mission_state = str(data['mission_state']).lower()
                            if mission_state == "start":
                                    mission_running = True
                            elif mission_state == 'stop':
                                mission_running = False

                elif(mission_running):
                    if( topic == 'observations/state'):
                        if('data' in json_line):
                                data = json_line['data']
                                if 'elapsed_milliseconds' in data:
                                    elapsed_milliseconds = int(data['elapsed_milliseconds'])
                    elif( topic == 'agent/gold'):                                                       
                        num_gold_messages+=1

        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        
        count += 1

    ######################################################################################
    # Do your testing of some aggregate value after all lines above have been processed here

    # SOME AGGREGATE TESTS HERE 

    out = 0

    boolean1 = False
    
    if (num_gold_messages != 0):
        
        boolean1 = (elapsed_milliseconds/num_gold_messages <= (1000*60*2) )
   
        out = (elapsed_milliseconds/num_gold_messages  )

    output[name+'_'+str(len(output.items()))] = name, str(boolean1) , '# avg ms/msg in mission : ' + str(int(out)) , 'max threshhold '+str(2*60*1000)+' ms/msg'  
   

    #######################################################################################
    # Write results to the global table that will print to a file   
    # where k is the id of the test
    # v is a tuple of length three [name,success,data,predicate] 
    # where name is the agent name, success is a boolean T/F, and data is extra data you've given to accompany the result   
    # output[agent_name_someint] = [ agent_name , str(true/False predicate) indicating success, some (short) extra string info for yourself,"#messages>7"]
    #######################################################################################
    for k, v in output.items():
        table[k]=v