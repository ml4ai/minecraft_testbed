
from ast import Return
import json, sys, traceback

ledger = { }

ac_filter_list = [
    'ac_cmu_ta2_ted',
    'AC_IHMC_TA2_Location-Monitor',
    'ac_cmu_ta2_beard',
    'AC_CMUFMS_TA2_Cognitive',
    'AC_Rutgers_TA2_Utility',
    'AC_Aptima_TA3_measures',
    'AC_CORNELL_TA2_TEAMTRUST',
    'AC_IHMC_TA2_Dyad-Reporting',
    'AC_CORNELL_TA2_ASI-FACEWORK',
    'AC_IHMC_TA2_Player-Proximity',
    'ac_ihmc_ta2_joint-activity-interdependence',
    'ac_gallup_ta2_gold',
    'PyGL_FoV_Agent',
    'ac_ucf_ta2_playerprofiler',
    'pygl_fov',
    'ac_gallup_ta2_gelp',
    'uaz_dialog_agent'
]

def updateLedger(sub_type:str):

    if( sub_type not in ledger):
        ledger[sub_type]=1
    else:
        ledger[sub_type]+=1

def main_parse(json_line)->any:
    
    if 'topic' in json_line:

        topic = json_line['topic']        

        if topic == "observations/events/player/victim_evacuated":

            json_line['topic'] = "observations/events/server/victim_evacuated"

            print ("Victim Evacuated topic fixed")

        elif topic == "trial":
            
            if('msg' in json_line):

                sub_type = json_line['msg']['sub_type']        
                
                if( sub_type == 'start' or sub_type == 'stop'):               
                        
                    if('client_info' in json_line['data']):                    
                        
                        client_info = json_line['data']['client_info']

                        new_client_info = []
                        
                        for info in client_info:
                            
                            if(info['playername']=='asist_advisor'):

                                print(' Removing asist_advisor from client_info.')
                                
                                updateLedger(json_line['msg']['sub_type']) 
                            else:
                                new_client_info.append(info)

                            # remove playername from client_info message
                            
                            json_line['data']['client_info'] = new_client_info

                    else:
                        print('------------------------------------------------------------------------')
                        print('Client Info not found in the data, must be an old trial. Reading supplied arguments')
        
        elif('msg' in json_line):

            msg = json_line['msg']  

            if ('source' in msg):

                source = msg['source']

                if ( source in ac_filter_list ):

                    if(source not in ledger.keys()):
                        ledger[source] = 1

                    else:
                        ledger[source] = ledger[source]+1
                    
                    return None

        
        return json_line

def parse_error(json_line:dict)->any:

    #print( json_line['msg']['sub_type'])

    error_dict:dict = json_line['error']
    data_string = error_dict['data']
    data_json = json.loads(data_string)
    json_line['data'] = data_json

    intermediate_json = main_parse(json_line)
    json_line['error'] = json.dumps(intermediate_json['data'])
    json_line.pop('data')
    
    return json_line

def cleanLine(json_line)->any:   

    if 'error' in json_line:
        # send to error handler
        return parse_error(json_line)
        
        #print(data_json)

    # checking via msg.subtype
    else:

       return main_parse(json_line)


if __name__ == "__main__":

    print('------------------------------------------------------------------------')
    print('Supplied Arguments : ')
    print(sys.argv)
    print(len(sys.argv))
    print('------------------------------------------------------------------------')


    incoming_file = sys.argv[1]
    outgoing_file = sys.argv[2]

    print("Cleaning file .... this will take a few seconds.")
    
    count = 0

    f = open(incoming_file, 'r',encoding='utf-8')

    lines = f.readlines()    

    print ( 'Read ' + str(len(lines)) + ' lines from source file.')

    f.close()

    f = open(outgoing_file, 'w' )

    # copy first line exactly

    f.write(lines[0])

    count += 1

    for i in range(len(lines)):

        #print("Line # " + str(i) )
        
        # skip first line
        if ( i == 0 ):
            continue    
            
        try:
            json_line = json.loads(lines[i])
        except Exception as e:
            print("Something went loading line : " + str(i))
            #print(json_line)
            traceback.print_exc()

        try:    
            clean_line = cleanLine(json_line)
        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()

        # write to new file
        if clean_line != None:
            f.write(json.dumps(clean_line))
            f.write('\n')
        
        count += 1

    f.close()


    print('------------------------------------------------------------------------')
    print ( ledger )
    print('------------------------------------------------------------------------')


    print ( 'Wrote ' + str(count) + ' lines to new file')
