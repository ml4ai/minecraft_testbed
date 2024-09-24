
import json,traceback

# agent/asr/final messages > 25
# agent/asr/intermediate messages >= 2*#agent/asr/final messages

def ac_uaz_ta1_speechanalyzer_test(name,lines,table:dict):

    # output is a dict used to store your result before putting it in the table at the end of this function
    # The key is the unqiue id of the test ( agent_name_int)
    # The value is a tuple of length three [agent_name,success,extra_data,predicate]    
    
    output={}

    count = 0

    # Add any variables you need to keep track of here    
    num_final_messages = 0    
    num_personality_messages = 0
    num_sentiment_messages = 0
    heartbeats = 0
    ver_info =0
    version = "Not Set"

    for i in range(len(lines)):
            
        # line to json
        json_line = json.loads(lines[i])

        try: 

            # do your line by line testing here to inform any aggregate tasks later on below                 
            if ('topic' in json_line):
                topic = str(json_line['topic']).lower()                 
                if(topic == 'agent/speech_analyzer/personality'):
                    num_personality_messages+=1
                elif(topic == 'agent/speech_analyzer/sentiment'):
                    num_sentiment_messages+=1
                elif(topic == 'agent/asr/final'):
                    num_final_messages+=1
                elif(topic == 'status/ac_uaz_ta1_speechanalyzer/heartbeats'):
                    heartbeats +=1
                elif(topic == "agent/ac_uaz_ta1_speechanalyzer/versioninfo"):
                    ver_info+=1
                    version = json_line['data']['version']


        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        
        count += 1

    ######################################################################################
    # Do your testing of some aggregate value after all lines above have been processed here

    # SOME AGGREGATE TESTS HERE

    boolean1 = num_final_messages == num_personality_messages
    boolean2 = num_final_messages == num_sentiment_messages
    boolean3 = heartbeats > 10
    boolean4 = ver_info > 0
    #######################################################################################

    output[name+'_'+str(len(output.items()))] = name, str(boolean1) , '# personality,# final msg: ' + str(num_personality_messages) +','+ str(num_final_messages),"# messages = #agent/asr/final messages"   
    output[name+'_'+str(len(output.items()))] = name, str(boolean2) , '# sentiment,# final msgs: ' + str(num_sentiment_messages) +','+ str(num_final_messages), "# messages = #agent/asr/final messages" 
    output[name+'_'+str(len(output.items()))] = name, str(boolean3) , '# heartbeats: ' + str(heartbeats),"# heartbeats > 10"  
    output[name+'_'+str(len(output.items()))] = name, str(boolean4) , '# Version: ' + str(version),"# ver info > 0"
    #######################################################################################
    # Write results to the global table that will print to a file   
    # where k is the id of the test
    # v is a tuple of length three [name,success,data,predicate] 
    # where name is the agent name, success is a boolean T/F, and data is extra data you've given to accompany the result   
    # output[agent_name_someint] = [ agent_name , str(true/False predicate) indicating success, some (short) extra string info for yourself,"#messages>7"]
    #######################################################################################
    for k, v in output.items():
        table[k]=v