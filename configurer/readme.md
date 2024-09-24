# Testbed Configure Tool

## Introduction

The testbed configure tool is used to setup the testbed by providing a single parameter file which can be used to update 
all of the config files in the testbed.  
If you are running on a single host Windows system, you should not need to do any configuration,
the default configuration should work.
If you are running on a single host Linux system, you can do all of the configuration with one python command.
```
cd configurer
python testbed_config.py -ip <host IP address>
```
The above command will edit all of the testbed component containers with the given
host IP address.  There is no need to edit the configurer .ini file (unless, for example, you are adding a new container).

If you have a change to the testbed configuration besides just the host IP, then you should
edit the main configure file and then run the tool.  The tool will update all of the specified config files with the
parameter values from the single config file.  You would need to do this in the case where you are running some
containers on one system and others on another systsem.

## Editing the config file
The single config file has the following format:
```
[configure]
testbed_local_root = <relative file path from where the configure tool is to the testbed Local directory>
manual_message = <notice to users of any manual configuration requirements that aren't handled by this configure file>

[section for one config file]
config_file = <relative path from Local to config file to be edited>
<property name>=<property value>
<property name>=<property value>
...

[section for next config file]
...
```
The current configure tool can handle editing .json and .env files based on the file extension of the config file.
The config files are edited by replacing the value of each property specified with the new value and then replace the config file in the same directory.

A templet file for a single node testbed is provided in `configurer/testbed_single_host.ini`.  

## Sequence to build and run the testbed using the configurer
This is the general sequences of tasks to start with a testbed distribution to get to a running testbed
1. Pull down the distrubtion from the git repository
2. Build all of the containers using `Local/testbed_build.cmd` (Windows) or `Local/testbed_build.sh` (Linux)
3. run the configurer tool
4. Start up the containers using `Local/testbed_up.cmd` (Windows) or `Local\testbed_up.sh` (Linux) 

## Running the tool (Detailed steps)
The configure tool is found in the `configurer` directory of the testbed distribution.
The tool is called testbed_config.py.
Python 3.\* is recommended, Python 2.\* has not been tested to run the tool.
To use the config tool, execute the following steps:
1. Edit the config file as described above to contain the values of the properties that you need for your configuration.  
The easist thing to do would be to start with the released .ini file and make the edits necessary for you configuration.
  a. The most common changes involve the MQTT broker ip address for non-Windows systems, 
    although depending on your configuration there may be other properties to set.
  b. Set the `testbed_local_root` property in the `configure` section to the relative path to the Local folder in your testbed distribution.

2. Run the configure tool.
The default config file is config.ini in the same directory the tool is run in.
You can also specify a config file on the command line for example `python testbed_config.py -cf testbed_single_host.ini`
As the configurer tool runs, it will report each of the config files that are being changed and the name and value of the properties that are changed.
