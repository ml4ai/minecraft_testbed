# -*- coding: utf-8 -*-
"""
.. module:: utils
   :platform: Linux, Windows, OSX
   :synopsis: A set of utility functions for ASIST agents

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>
"""

import argparse
import glob
import itertools
import json
import os
import re
import sys

from .config_loader import ConfigLoader

from MinecraftBridge.utils import Loggable
from MinecraftBridge.mqtt import (
    Bridge as MessageBusBridge,
    FileBridge
)
from pathlib import Path



def parseCommandLineArguments(**kwargs):
    """
    Create an ArgumentParser and parse the arguments.

    Keyword Arguments
    -----------------
    additional_parser_configuration : function
        Function to call to add optional arguments to the parser prior to
        parsing.  The provided function must take an `ArgumentParser` instance
        in as an argument, and returns nothing

    Return
    ------
    args : argparse.Namespace
        A namespace containing parsed arguments
    config : dictionary
        A dictionary of the loaded config file

    Namespace Attributes
    --------------------
    config_file : string
        path to the JSON configuration file
    input_file : string, optional
        path to an input metadata file
    output_file : string, optional
        path to an output metadata file
    """

    # Set up the parser
    parser = argparse.ArgumentParser(description='TemplateAgent')
    parser.add_argument('config_file', help='Path to the config file.')
    parser.add_argument('--input_file', '-i', help='Input metadata file, for file replay.')
    parser.add_argument('--output_file', '-o', help='Output metadata file, for file replay.')

    # Add any additional arguments to the parser, if provided
    additional_config = kwargs.get("additional_parser_configuration", None)
    if additional_config is not None:
        additional_config(parser)


    args = parser.parse_args()

    if not os.path.exists(args.config_file):
        print("ERROR:  Config file does not exist: %s" % args.config_file)
        sys.exit(1)

    config_path, config_filename = os.path.split(args.config_file)
    configLoader = ConfigLoader(working_directory=config_path)
    config = configLoader.load(config_filename)

    # Initialize the loggers, if provided in the config file
    Loggable.configure(config.get("loggers", {}))

    # Check to see if an input and output file have been provided -- both are
    # required at the moment
    if args.input_file and not args.output_file:
        args.output_file = os.devnull
###        sys.exit(1)
    if not args.input_file and args.output_file:
        print("ERROR: Output file provided without input metadata file!  Exiting.")
        sys.exit(1)

    # Get the agent name
    agent_name = config.get('agent_name', 'UNNAMED_AGENT')

    # Create a FileBridge if input and output files are provided
    if args.input_file and args.output_file:
        minecraft_bridge = FileBridge(agent_name,
                            args.input_file,
                            args.output_file)
    # Create a MQTT Message Bus if not
    else:
        mqtt_bus = config.get('mqtt_bus', {'host': 'localhost', 'port': 1883})
        host = mqtt_bus.get('host', 'localhost')
        port = int(mqtt_bus.get('port', 1883))
        minecraft_bridge = MessageBusBridge(agent_name, host, port)


    # Return the parsed arguments
    return args, config, minecraft_bridge


def get_metadata_paths(
    data_dir, file_pattern='NotHSRData_TrialMessages_Trial-*.metadata'):
    """
    Get a list of metadata paths from a directory, one for each trial.
    If multiple versions of a trial are present, choose the latest version.

    Arguments
    ---------
    data_dir : string
        path to directory containing metadata paths
    file_pattern : string
        a glob pattern to select filenames
    """
    all_metadata_paths = glob.glob(str(Path(data_dir) / file_pattern))
    all_metadata_paths = [path for path in all_metadata_paths if 'aborted' not in path]

    # Get the latest version for each trial
    pattern = r'Trial-T([0-9]+)_.*_Vers-([0-9]+).metadata' # match (trial, version)
    trial_info = [(path, re.findall(pattern, path)) for path in all_metadata_paths] # list of (path, search)
    trial_info = [(path, *r[0]) for path, r in trial_info if r] # list of (path, trial, version)
    trial_info = sorted(trial_info, key=lambda x: x[1]) # sort by trial
    trial_groups = itertools.groupby(trial_info, key=lambda x: x[1]) # group by trial
    metadata_paths = [max(group, key=lambda x: x[2])[0] for _, group in trial_groups] # max version
    return sorted(metadata_paths)
