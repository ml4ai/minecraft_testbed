import configparser
import argparse
import pprint
import json
import re

def parse_command_line_args():
	parser = argparse.ArgumentParser(description='ASIST testbed config tool')
	parser.add_argument('-cf', '--config_file', dest='config_file', default='testbed_single_host.ini',help='the config file name')
	parser.add_argument('-ip', '--ip', dest='host_ip', help='the IP address of the testbed host')

	return parser.parse_args()

def fix_json_config(data, config_section):
	for item in config_section.keys():
		print("Changing {item} to new value: {value}".format(item=item, value=config_section[item]))
		nests = item.split(".")
		if len(nests) > 2:
			print("*** ERROR: only 2 level nested properties supported: {item}***".format(item=item))
		if len(nests) == 1:
			data[item] = config_section[item]
		else:
			data[nests[0]][nests[1]] = config_section[item]
	return data

def get_env_data(cf):
	#open the file
	envre = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')
	result = {}
	with open(cf) as ins:
		for line in ins:
			match = envre.match(line)
			if match is not None:
				result[match.group(1)] = match.group(2)
	return result
		

def fix_env_config(data, config_section):
	for item in config_section.keys():
		print("Changing {item} to new value: {value}".format(item=item, value=config_section[item]))
		data[item] = config_section[item]
	return data

def write_new_json(cf, data):
	#cf = cf + "-edited"
	print("Saving config file: {cf}".format(cf=cf))
	with open(cf, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)

def write_new_env(cf, data):
	#cf = cf + "-edited"
	print("Saving config file: {cf}".format(cf=cf))
	with open(cf, 'w', encoding='utf-8') as f:
		for key, value in data.items():
			f.write("{key}={value}\n".format(key=key,value=value))
def edit_config_file(config_file, edited_config_file, host_ip):
	f_config_file = open(config_file,"r")
	f_config_file_edited = open(edited_config_file, "w")
	line = f_config_file.readline()
	while line:
		if host_ip != None:
			line1 = line.replace("host.docker.internal",host_ip)
			line2 = line1.replace("localhost", host_ip)
		else:
			line2 = line
		f_config_file_edited.write(line2)
		line = f_config_file.readline()

	f_config_file.close()
	f_config_file_edited.close()

pp = pprint.PrettyPrinter(indent=4)
cmd_args = parse_command_line_args()
print("Command args")
pp.pprint(cmd_args)
#edit the config file and fix the IP address
edited_config_file = "edited_config_file.ini"
edit_config_file(cmd_args.config_file, edited_config_file, cmd_args.host_ip)

config = configparser.RawConfigParser()
config.optionxform = lambda option: option
print("Using config file: {config_file}.".format(config_file=cmd_args.config_file))
config.read(edited_config_file)

#check to see if we found a config file
if not "configure" in config:
	print("No configure file found. Exiting")
	quit()

#pp.pprint({section: dict(config[section]) for section in config.sections()})

#print out any  manual configuration note from the configure section
if 'manual_message' in config['configure']:
	print("Manual configuration steps not performed by this tool:") 
	print(config['configure']['manual_message'])
	
#get the sections from the config file
sections = config.sections()
sections.remove('configure')

config_root = config['configure']['testbed_local_root']
print("testbed_local_root:{tlr}".format(tlr=config_root))
print("======")
for section in sections:
	print("Working on config section: {section}".format(section=section))
	
	#build the file spec for the config file
	cf = config_root + config[section]['config_file']
	#remove the config_file property for the section so it doesn't get added to the actual config file
	config[section].pop('config_file')
	
	#print("Config file spec:{cfs}".format(cfs=cf))
	
	#open the config file to make edits
	with open(cf) as f:
		file_ext = re.search("\.([a-zA-Z0-9]*)$", cf).group()
		if file_ext == ".json":
			print("Fixing config file: {cf}".format(cf=cf))
			data = json.load(f)
			#pp.pprint(data)
			#print("++++++")
			#now fix the json with the updated config data
			fixed_data = fix_json_config(data, config[section])
			#pp.pprint(fixed_data)
			write_new_json(cf,fixed_data)
		if file_ext == ".env":
			print("Fixing config file: {cf}".format(cf=cf))
			data = get_env_data(cf)
			#pp.pprint(data)
			#print("++++++")
			fixed_data = fix_env_config(data,config[section])
			#pp.pprint(fixed_data)
			write_new_env(cf,fixed_data)
		print("+=====")
