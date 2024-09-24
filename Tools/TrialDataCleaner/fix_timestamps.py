
import json, sys, traceback
from datetime import datetime,timedelta

starting_timestamp:datetime = None
last_insync_timestamp:datetime = None
time_threshhold:timedelta = timedelta(hours=12)
cached_out_of_sync = []
correction_count = 0

# Some timestamps have too much precision for datetime.strptime, so we 
# are removing anything more precise than a microsecond -- .000000Z
def checkString(string_date)->str:

    splitString = str.split(string_date,'.')
    splitString = splitString

    # If has no milliseconds wil fail to parse
    if ( len(splitString)<2 ):
        # split on colon and grab the last index
        no_milli_split = str.split(string_date,':')
        last_part = no_milli_split[len(no_milli_split)-1]

        #insert some milliseconds
        index = last_part.find('Z')
        last_part = last_part[:index] + '.000Z'
        no_milli_split[len(no_milli_split)-1] = last_part

        # print(':'.join(no_milli_split))
        
        return( ':'.join(no_milli_split) )
    
    # precisions greater than microseconds won't parse
    if ( len(splitString[1])>7 ):
        #print("Found too much precision ... correcting")
        #print(str(splitString))
        splitString[1] = splitString[1][0:6] + 'Z'
        #print( '.'.join(splitString) )
        return( '.'.join(splitString) )
    
    else:
        return string_date
    

# Parse the string representation of the date into something we can understand
def parseDate(string_date)->datetime:    
   
    out = None
    checked_string = checkString(string_date)

    try:
        out = datetime.strptime(checked_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    except Exception as e:
        
        print(e)        

    return out
    
# Apply a threshold check to see if this is an out of sync timestamp
def check_time_out_of_sync(time:datetime)->bool:
    global starting_timestamp
    global time_threshhold
    if( time > (starting_timestamp+time_threshhold) ):        
        return True
    return False

# Distributes an equal "step" of time to each of the timestamps in the out of sync cache according to
# step = timedelta/len(out-of-sync cache) ... ie 900 ms timedelta for cache of length three would yeild
# timestamps like so : [lastInSyncTimestamp + 300,lastInSyncTimestamp + 600, lastInSyncTimestamp + 900]
def distribute_time_evenly( parsedDate:datetime, last_insync_timestamp:datetime)->list:
    global cached_out_of_sync

    delta:timedelta = parsedDate - last_insync_timestamp
    # convert delta to microseconds, then subtact 1 millisecond so the final entry is not the same as the next insync timestamp
    delta_micro = (delta.total_seconds() * 1000000) - 1000
    micro_step = delta_micro / len(cached_out_of_sync)

    #print ( "Delta_Micro : " + str(delta_micro) + " / Micro Step : " + str(micro_step))

    step_datetime = last_insync_timestamp + timedelta(microseconds=micro_step)
    for line in cached_out_of_sync:
        stepped_time_as_string = step_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        line['header']['timestamp'] = stepped_time_as_string
        line['msg']['timestamp'] = stepped_time_as_string
        #print ("Stepped time : " + stepped_time_as_string)
        step_datetime = step_datetime + timedelta(microseconds=micro_step)
    return cached_out_of_sync

# the main part of the program, ingests a line and line number, checks the timestamp
# keeps track of the last insync stamp, caches all out of sync messages, then updates them on finding
# the next insync timestamp
def main_parse(json_line:dict, line_number:int)->any:
    
    global starting_timestamp
    global last_insync_timestamp
    global time_threshhold
    global cached_out_of_sync
    global correction_count
    
    if ( starting_timestamp == None) :
        print( 'Starting Timestamp not set')
     
    
    if 'topic' in json_line:
        
        topic = json_line['topic']
        
        if topic == 'trial' and json_line['msg']['sub_type']=='start' :
            string_time = json_line['header']['timestamp']
            starting_timestamp = parseDate(string_time)  
            last_insync_timestamp = starting_timestamp
            print( "Starting Timesamp set as : " + str(starting_timestamp ))
        
        if ('header' in json_line) and ('timestamp' in json_line['header']) and (starting_timestamp!=None):

            parsedDate = parseDate( json_line['header']['timestamp'] )
        
            # if out of sync, cache it until we hit the the next insync one
            if ( check_time_out_of_sync( parsedDate ) ):
                
                #print ("Out of sync time found on line " + str(line_number))
                cached_out_of_sync.append(json_line)

                correction_count += 1
            else:
                # must do this if check - sometimes header dates are out of order by a few milliseconds and we don't want that to
                # be the one we use as its negative time
                if(parsedDate > last_insync_timestamp):
                    # if in sync, dump the corrected cache if it exists, then write this line at the end                    
                    if(len(cached_out_of_sync)>0):
                        # make sure to maintain order according to header timestamps
                        cached_out_of_sync.sort( key=lambda d: datetime.strptime(checkString(d['header']['timestamp']), "%Y-%m-%dT%H:%M:%S.%fZ") )
                        fixed_cache = distribute_time_evenly( parsedDate,last_insync_timestamp)
                        # at this point its a good idea to resort according to @timestamp to maintain consistency
                        # fixed_cache.sort( key=lambda d: datetime.strptime(checkString(d['@timestamp']), "%Y-%m-%dT%H:%M:%S.%fZ") )
                        for line in fixed_cache:
                            f.write(json.dumps(line)+"\n")
                    cached_out_of_sync.clear()
                    last_insync_timestamp = parsedDate        
                    #print ("Set new last_insync_time " + str(parsedDate))
                    f.write(json.dumps(json_line)+"\n")
                # write things that are negative time by milliseconds directly, don't set them to last insync timestamp
                else:
                    f.write(json.dumps(json_line)+"\n")
        
    
            
               

    
def cleanLine(json_line:dict, line_number:int, f)->any:   

    return main_parse(json_line,line_number)


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

    f = open(outgoing_file, 'w',encoding='utf-8')    

    count += 1

    for i in range(len(lines)):

        #print("Line # " + str(i) )
        
        # skip first line
        if ( i == 0 ):
            f.write( lines[0] )    
            pass
        # line to json
        json_line:dict = json.loads(lines[i])

        try:    
            cleanLine(json_line,i+1,f)
        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
            sys.exit()
        count += 1
    
    f.close()

    print(" --------- Corrected " + str(correction_count) + " timestamps using the even distribution method. ---------- ")





 
