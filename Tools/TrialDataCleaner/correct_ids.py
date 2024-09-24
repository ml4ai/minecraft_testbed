
from ast import Return
import json, sys, traceback

ids_set = False
ledger:dict = {}
ledger["replay_id"]={}
ledger["replay_parent_id"]={}
ledger["replay_parent_type"]={}
has_export_message = False
export_message = "NOT SET"
TRIAL_ID = "NOT SET"
TRIAL_REPLAY_ID = "NOT SET"
TRIAL_REPLAY_PARENT_ID = "NOT SET"
TRIAL_REPLAY_PARENT_TYPE = "NOT SET"

header = {

    "timestamp": "2022-04-15T00:35:57.890Z",
    "message_type": "export",
    "version": "3.5.3-dev-94-gad305995"
}
msg = {

    "sub_type": "replay",
    "source": "metadata-web",
    "experiment_id": "NOT SET",
    "trial_id": "NOT SET",
    "timestamp": "NOT SET",
    "version": "3.5.3-dev-94-gad305995",
    "replay_id": "NOT SET",
    "replay_parent_id": "NOT SET",
    "replay_parent_type": "TRIAL"
}
data = {
    "index": "logstash-2022.04.14-000001",
    "ignore_message_list": [],
    "ignore_source_list": [            
    ],
    "ignore_topic_list": [],
    "metadata": {
        "replay": {
            "id": 1,
            "replay_id": "NOT SET",
            "replay_parent_id": "NOT SET",
            "replay_parent_type": "TRIAL",
            "date": "NOT SET",
            "ignore_message_list": [],
            "ignore_source_list": [                    
            ],
            "ignore_topic_list": []
        },
        "parents": [
            {
                "id": 1,
                "trial_id": "NOT SET",
                "name": "NOT SET",
                "date": "NOT SET",
                "experimenter": "NOT SET",
                "subjects": [],
                "trial_number": "NOT SET",
                "group_number": "NOT SET",
                "study_number": "NOT SET",
                "condition": "NOT SET",
                "notes": [
                    "na"
                ],
                "testbed_version": "3.5.2-dev-328-g050fa5b",
                "experiment": {
                    "id": 1,
                    "experiment_id": "NOT SET",
                    "name": "NOT SET",
                    "date": "NOT SET",
                    "author": "NOT SET",
                    "mission": "NOT SET"
                }
            }
        ]
    }
}

canned_export_message:dict = {
    "header" : header,
    "msg" : msg,
    "data" : data
}

def set_export_message(json_line:dict)->dict:
    global canned_export_message

    timestamp = json_line["msg"]["timestamp"]
    trial_id = json_line["msg"]["trial_id"]
    experiment_id = json_line["msg"]["experiment_id"]
    replay_id = json_line["msg"]["replay_id"]
    replay_parent_id = json_line["msg"]["trial_id"]

    #msg
    canned_export_message["msg"]["timestamp"] = timestamp
    canned_export_message["msg"]["experiment_id"] = experiment_id
    canned_export_message["msg"]["trial_id"] = trial_id
    canned_export_message["msg"]["replay_id"] = replay_id
    # because the parent is a trial we need to do it as below - also the trail messages had this incorrect for many
    canned_export_message["msg"]["replay_parent_id"] = trial_id

    #data
    canned_export_message["data"]["metadata"]["replay"]["replay_id"] = replay_id
    canned_export_message["data"]["metadata"]["replay"]["replay_parent_id"] = replay_parent_id
    canned_export_message["data"]["metadata"]["replay"]["date"] = timestamp

    canned_export_message["data"]["metadata"]["parents"][0]["trial_id"] = trial_id
    canned_export_message["data"]["metadata"]["parents"][0]["name"] = json_line["data"]["name"]
    canned_export_message["data"]["metadata"]["parents"][0]["date"] = json_line["data"]["date"]
    canned_export_message["data"]["metadata"]["parents"][0]["experimenter"] = json_line["data"]["experimenter"]
    canned_export_message["data"]["metadata"]["parents"][0]["subjects"] = json_line["data"]["subjects"]
    canned_export_message["data"]["metadata"]["parents"][0]["trial_number"] = json_line["data"]["trial_number"]
    canned_export_message["data"]["metadata"]["parents"][0]["group_number"] = json_line["data"]["group_number"]
    canned_export_message["data"]["metadata"]["parents"][0]["study_number"] = json_line["data"]["study_number"]
    canned_export_message["data"]["metadata"]["parents"][0]["condition"] = json_line["data"]["condition"]

    canned_export_message["data"]["metadata"]["parents"][0]["experiment"]["experiment_id"] = experiment_id
    canned_export_message["data"]["metadata"]["parents"][0]["experiment"]["name"] = json_line["data"]["experiment_name"]
    canned_export_message["data"]["metadata"]["parents"][0]["experiment"]["date"] = json_line["data"]["date"]
    canned_export_message["data"]["metadata"]["parents"][0]["experiment"]["author"] = json_line["data"]["experimenter"]
    canned_export_message["data"]["metadata"]["parents"][0]["experiment"]["mission"] = json_line["data"]["condition"]

    return canned_export_message

def main_parse(json_line)->any:    

    global ids_set 
    global has_export_message
    global export_message
    global ledger
    global TRIAL_ID
    global TRIAL_REPLAY_ID
    global TRIAL_REPLAY_PARENT_ID
    global TRIAL_REPLAY_PARENT_TYPE


    if  not ids_set and 'header' in json_line:
        header = json_line['header']
        if 'message_type' in header:
            if header['message_type'] == 'export':                
                has_export_message = True
                export_message = json_line
                TRIAL_ID = json_line['msg']['trial_id'] 
                TRIAL_REPLAY_ID = json_line['msg']['replay_id'] 
                TRIAL_REPLAY_PARENT_ID = json_line['msg']['replay_parent_id']
                TRIAL_REPLAY_PARENT_TYPE = json_line['msg']['replay_parent_type']
                ids_set = True

    
    if 'msg' in json_line :
        msg = json_line['msg']
        if 'replay_id' in msg:
            replay_id = msg['replay_id']
            if replay_id != TRIAL_REPLAY_ID:
                json_line['msg']['replay_id'] = TRIAL_REPLAY_ID
            if( replay_id not in ledger['replay_id']):
                ledger["replay_id"][replay_id] = 1
            else:  
                ledger["replay_id"][replay_id] += 1
        if 'replay_parent_id' in msg:
            replay_parent_id = msg['replay_parent_id']
            if replay_parent_id != TRIAL_REPLAY_PARENT_ID:
                json_line['msg']['replay_parent_id'] = TRIAL_REPLAY_PARENT_ID
            if( replay_parent_id not in ledger['replay_parent_id']):
                ledger["replay_parent_id"][replay_parent_id] = 1
            else:  
                ledger["replay_parent_id"][replay_parent_id] += 1 
        if 'replay_parent_type' in msg:
            replay_parent_type = msg['replay_parent_type']
            if replay_parent_type != TRIAL_REPLAY_PARENT_TYPE:
                json_line['msg']['replay_parent_type'] = TRIAL_REPLAY_PARENT_TYPE
            if( replay_parent_type not in ledger['replay_parent_type']):
                ledger["replay_parent_type"][replay_parent_type] = 1
            else:  
                ledger["replay_parent_type"][replay_parent_type] += 1           


        
    return json_line

def parse_error(json_line:dict)->any:

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
        
        return parse_error(json_line)
    
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

    for i in range(len(lines)):
            
        try:
            json_line = json.loads(lines[i])
            # CHECK IF WE HAVE AN EXPORT LINE
            if i == 0:
                print( "-------------------------0---------------------------")
                print( "-------------------------"+ header['message_type'] +"---------------------------")
                header = json_line['header']
                if 'message_type' in header:
                    if header['message_type'] != 'export':
                        print( "-------------------------NOT EQUAL TO EXPORT!---------------------------")
                        index = i
                        trial_message_found = False
                        while not trial_message_found:
                            if header['message_type'] == 'trial':
                                trial_message_found = True
                                export_line:dict = set_export_message(json.loads(lines[index]))
                                export_line_parsed = cleanLine(export_line)
                                f.write(json.dumps(export_line_parsed))
                                f.write('\n')
                                count +=1
                            else:
                                index +=1
                    

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
    print( " EXPORT MESSAGE PRESENT : " + str(has_export_message))
    print ( "TRIAL_ID : " + TRIAL_ID + " TRIAL_REPLAY_ID : " + TRIAL_REPLAY_ID + " TRIAL_REPLAY_PARENT_ID : " + TRIAL_REPLAY_PARENT_ID + " TRIAL_REPLAY_PARENT_TYPE : " + TRIAL_REPLAY_PARENT_TYPE )
    for s in ledger:
        print ( s, ledger[s] )
    print('------------------------------------------------------------------------')

    print ( 'Wrote ' + str(count) + ' lines to new file')
