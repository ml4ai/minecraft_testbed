import json,traceback

# # messages == 1

def ac_ihmc_ta2_location_monitor_test(name,lines,table:dict):

    # output is a dict used to store your result before putting it in the table at the end of this function
    # The key is the unqiue id of the test ( agent_name_int)
    # The value is a tuple of length three [agent_name,success,extra_data,predicate]    
    
    output={}

    count = 0

    # Add any variables you need to keep track of here    
    num_map_init_messages = 0
    num_loc_messages = 0

    for i in range(len(lines)):
            
        # line to json
        json_line = json.loads(lines[i])

        try: 

            # do your line by line testing here to inform any aggregate tasks later on below                 
            if ('topic' in json_line):
                topic = str(json_line['topic']).lower()
                if(topic == 'ground_truth/semantic_map/initialized'):
                    num_map_init_messages+=1
                elif(topic == 'observations/events/player/location'):
                    num_loc_messages+=1


        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        
        count += 1

    ######################################################################################
    # Do your testing of some aggregate value after all lines above have been processed here

    # SOME AGGREGATE TESTS HERE
    boolean1 = (num_map_init_messages==1)  
    
    
    boolean2 = (num_loc_messages>=500) 

    #######################################################################################

    output[name+'_'+str(len(output.items()))] = name, str(boolean1) , '# num sem_map_ini messages : ' + str(num_map_init_messages),"# messages == 1"   
    output[name+'_'+str(len(output.items()))] = name, str(boolean2) , '# num player loc messages : ' + str(num_loc_messages),"# loc messages >= 500" 
    #######################################################################################
    # Write results to the global table that will print to a file   
    # where k is the id of the test
    # v is a tuple of length three [name,success,data,predicate] 
    # where name is the agent name, success is a boolean T/F, and data is extra data you've given to accompany the result   
    # output[agent_name_someint] = [ agent_name , str(true/False predicate) indicating success, some (short) extra string info for yourself,"#messages>7"]
    #######################################################################################
    for k, v in output.items():
        table[k]=v