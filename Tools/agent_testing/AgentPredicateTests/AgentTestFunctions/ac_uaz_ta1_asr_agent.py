
import json,traceback

# agent/asr/final messages > 25
# agent/asr/intermediate messages >= 2*#agent/asr/final messages

def ac_uaz_ta1_asr_agent_test(name,lines,table:dict):

    # output is a dict used to store your result before putting it in the table at the end of this function
    # The key is the unqiue id of the test ( agent_name_int)
    # The value is a tuple of length three [agent_name,success,extra_data,predicate]    
    
    output={}

    count = 0

    # Add any variables you need to keep track of here    
    num_final_messages = 0
    num_interm_messages = 0

    for i in range(len(lines)):
            
        # line to json
        json_line = json.loads(lines[i])

        try: 

            # do your line by line testing here to inform any aggregate tasks later on below                 
            if ('topic' in json_line):
                topic = str(json_line['topic']).lower()                 
                if(topic == 'agent/asr/intermediate'):
                    num_interm_messages+=1
                elif(topic == 'agent/asr/final'):
                    num_final_messages+=1


        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        
        count += 1

    ######################################################################################
    # Do your testing of some aggregate value after all lines above have been processed here

    # SOME AGGREGATE TESTS HERE
    error_margin = 0.10
    message_margin = int(error_margin*num_final_messages)
    lower_bound = num_final_messages - message_margin
    upper_bound = num_final_messages + message_margin    

    boolean1 = num_final_messages>25
    boolean2 = num_interm_messages >= lower_bound and num_interm_messages <= upper_bound 

    #######################################################################################

    output[name+'_'+str(len(output.items()))] = name, str(boolean1) , '# final msgs : ' + str(num_final_messages), "# messages > 25"   
    output[name+'_'+str(len(output.items()))] = name, str(boolean2) , '# interm msgs : ' + str(num_interm_messages), "# messages = #agent/asr/final messages +- 10%"   
    #######################################################################################
    # Write results to the global table that will print to a file   
    # where k is the id of the test
    # v is a tuple of length three [name,success,data,predicate] 
    # where name is the agent name, success is a boolean T/F, and data is extra data you've given to accompany the result   
    # output[agent_name_someint] = [ agent_name , str(true/False predicate) indicating success, some (short) extra string info for yourself,"#messages>7"]
    #######################################################################################
    for k, v in output.items():
        table[k]=v
