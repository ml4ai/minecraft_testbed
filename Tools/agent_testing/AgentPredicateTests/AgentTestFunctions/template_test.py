
import json,traceback

# This is a template test function to use as a reference for an automated test of your agent.
# Once you have customized this function to your needs, add it to the tests array in
# "run_agent_tests.py" and it will automatically append to the output table and file

def template_test(name,lines,table:dict):

    # output is a dict used to store your result before putting it in the table at the end of this function
    # The key is the unqiue id of the test ( agent_name_int)
    # The value is a tuple of length three [agent_name,success,extra_data,predicate]    
    
    output={}

    count = 0

    # Add any variables you need to keep track of here
    
    for i in range(len(lines)):
            
        # line to json
        json_line = json.loads(lines[i])

        try: 

            # do your line by line testing here to inform any aggregate tasks later on below                 
            if ( ('topic' in json_line) and ('data' in json_line) ):
                print("Do a test")


        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        
        count += 1

    ######################################################################################
    # Do your testing of some aggregate value after all lines above have been processed here

    # SOME AGGREGATE TESTS HERE

    #######################################################################################

    #######################################################################################
    # Write results to the global table that will print to a file   
    # where k is the id of the test
    # v is a tuple of length three [name,success,data,predicate] 
    # where name is the agent name, success is a boolean T/F, and data is extra data you've given to accompany the result   
    # output[agent_name_someint] = [ agent_name , str(true/False predicate) indicating success, some (short) extra string info for yourself,"#messages>7"]
    #######################################################################################
    for k, v in output.items():
        table[k]=v


    

    
    



