#!/usr/bin/env python

# FOR TESTING FUNCTIONALITY ON LOCAL METADATA FILES

from argparse import ArgumentParser
import configparser
import cProfile
import json
import logging
import os.path
import sys
import glob
import traceback

from atomic.parsing.asist_world import ASISTWorld

#metadata_file = '/home/ubuntu/metadata_files/s3_pilot.meta'
metadata_file = '/home/ubuntu/metadata_files/s3_study.meta'
asistWorld = ASISTWorld()

numres = 0

with open(metadata_file, 'rt') as json_file:
    for line_no, line in enumerate(json_file):
        try:
            msg = json.loads(line)
        except Exception:
            print("can't load msg:: "+str(line))
            msg = None
        if msg:
            #print('message == '+str(msg))
            res = asistWorld.process_msg(msg)
            if res:
                numres += 1
                print("message was:: "+str(msg))
                print("subtype :: "+str(msg['msg']['sub_type']))
                print("topic :: "+str(msg['topic']))                      
                print("RESULT:: "+str(res))
    #asistWorld.process_stop(
    print("TOTAL RES:: "+str(numres))
