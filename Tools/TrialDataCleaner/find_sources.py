
import json, sys, traceback

sources = set()



def main_parse(json_line)->any:
    
    if 'msg' in json_line :

        msg = json_line['msg']

        if 'source' in msg:
            source = msg['source']
            sources.add(source)       

def cleanLine(json_line)->any:   

    return main_parse(json_line)


if __name__ == "__main__":

    print('------------------------------------------------------------------------')
    print('Supplied Arguments : ')
    print(sys.argv)
    print(len(sys.argv))
    print('------------------------------------------------------------------------')


    incoming_file = sys.argv[1]
    

    print("Cleaning file .... this will take a few seconds.")
    
    count = 0

    f = open(incoming_file, 'r',encoding='utf-8')

    lines = f.readlines()    

    print ( 'Read ' + str(len(lines)) + ' lines from source file.')

    f.close()

    count += 1

    for i in range(len(lines)):

        #print("Line # " + str(i) )
        
        # skip first line
        if ( i == 0 ):
            continue    
            
        # line to json
        json_line = json.loads(lines[i])

        try:    
            clean_line = cleanLine(json_line)
        except Exception as e:
            print("Something went wrong on line : " + str(i))
            #print(json_line)
            traceback.print_exc()
        count += 1


    print('------------------------------------------------------------------------')

    for s in sources:
        print ( s )
    print('------------------------------------------------------------------------')


 
