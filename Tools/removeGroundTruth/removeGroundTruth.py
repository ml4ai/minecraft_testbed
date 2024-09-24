# Remove ground truth from ASIST metadata file of testbed messages
# arguments
#   -i input directory to find the files to be processed
#   -o output directory to write the processed files

import argparse, json, os, sys

#define and parse the command line arguments
def parse_command_line_args():
	parser = argparse.ArgumentParser(description='ASIST clean ground truth tool')
	parser.add_argument('-i','--input', dest='input_dir', required=True, help='The input directory to be processed')
	parser.add_argument('-o','--output', dest='output_dir', required=True, help='The output directory to place processed files')

	return parser.parse_args()

#clean the ground truth out of the message in json_line
def process_message(json_line)->any:
    if'data' in json_line:
        if 'msg' in json_line:
            #remove the ground truth from the trial start and stop messages
            if(json_line['msg']['sub_type'] == 'start') or (json_line['msg']['sub_type'] == 'stop'):
                    
                if('client_info' in json_line['data']):
                    print( "Client Info in trial message found!")
                    
                    client_info = json_line['data']['client_info']
                    
                    for info in client_info:
                        
                        # remove staticmapversion from client_info message
                        if 'staticmapversion' in info:
                            info.pop('staticmapversion')
                        #remove markerblocklegend from client_info messages
                        if 'markerblocklegend' in info:
                            info.pop('markerblocklegend')
                        
            #remove the measures message
            if (json_line['msg']['sub_type'] == 'measures' ):
                meas = json_line['data']
                if 'M1' in meas:
                    meas.pop('M1')
                if 'M2' in meas:
                    meas.pop('M2')
                if 'M3' in meas:
                    meas.pop('M3')
                if 'M4' in meas:
                    meas.pop('M4')
                if 'M5' in meas:
                    meas.pop('M5')
                if 'M6' in meas:
                    meas.pop('M6')
                if 'M7' in meas:
                    meas.pop('M7')
                print("Remove measure ground truth for trial")
    return json_line

def generate_output_file(in_file_name):
    f_parts = in_file_name.partition('Vers-')
    #f_parts should contain the main file name part, the string "Vers-" and then the version number and .metadata
    #get the version part
    ver = f_parts[2].split(".")[0]
    updated_ver_str = str(int(ver[0])+1)
    print(f"old Ver: {ver[0]}, new ver: {updated_ver_str}")
    return f_parts[0] + "Vers-" + updated_ver_str + ".metadata"
	
#clean the ground truth from a given file
def clean_file(input_dir, msg_file, output_dir):
    file_to_open = os.path.join(input_dir, msg_file.name)
    print('------------------------------------------------------------------------')
    print(file_to_open)
    output_file_name = generate_output_file(msg_file.name)
    f_out = open(os.path.join(output_dir,output_file_name),'w+')
    print(f"Output file: {output_file_name}")
    with open(file_to_open) as f:
        for line in f:
            j_line = json.loads(line)
            out_line = process_message(j_line)
            out_line_str = json.dumps(out_line)

            #remove the spaces that json.dumps puts in
            cleaned_out_line = out_line_str.replace('": ', '":').replace(', ',',')
            f_out.write(cleaned_out_line)
            f_out.write('\n')
    f_out.close()



def main():

    config = {}

    #get the command line arguments
    cmd_args = parse_command_line_args()
    #print(cmd_args)
    
    if cmd_args.input_dir != None:
        config["input_dir"] = cmd_args.input_dir
    if cmd_args.output_dir != None:
        config["output_dir"] = cmd_args.output_dir

    #set up loop through all of the files in the input directory
    with os.scandir(config["input_dir"]) as msg_files:
        for msg_file in msg_files:
            #print(msg_file.name)
            if msg_file.is_dir():
                continue
            if msg_file.name.endswith(".metadata") and "Saturn" in msg_file.name:
                print("Processing file: " + msg_file.name)
                clean_file(config["input_dir"], msg_file, config["output_dir"])


if __name__ == '__main__':
    main()
