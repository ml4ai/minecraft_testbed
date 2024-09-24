#!/usr/bin/env python

import os.path
import json
from atomic.analytic.ihmc_wrapper import JAGWrapper
from atomic.analytic.gallup_wrapper import GelpWrapper
from atomic.analytic.corenll_wrapper import ComplianceWrapper
from atomic.analytic.cmu_wrapper import TEDWrapper

class atomicParser:

    def __init__(self):
        self.ac_filters = {
            'ihmc':{'observations/events/player/jag', 'observations/events/mission',
                    'observations/events/player/role_selected'}, 
            'cornell':{'agent/ac/player_compliance'},
            'cmu_ted':{'agent/ac/cmuta2-ted-ac/ted'},
            'gallup':{'agent/gelp'}
        }
        self.ac_wrappers = {
            'ihmc':JAGWrapper('ihmc', 'jag'),
            'cornell': ComplianceWrapper('cornell', 'compliance'),
            'cmu_ted': TEDWrapper('cmu', 'ted'), 
            'gallup': GelpWrapper('gallup', 'gelp')
        }

    def proc_msg_psim(self, msg_topic, jmsg="DEFAULT MSG"):
        for ac_name, topics in self.ac_filters.items(): # check this in live atomic_parser??
            # print("===>> in proc_msg curr topic == "+str(msg_topic)+" ALL topics == "+str(topics))
            if (msg_topic == 'trial') or (msg_topic in topics):
                self.ac_wrappers[ac_name].handle_message(msg_topic, jmsg['msg'], jmsg['data'])

if __name__ == '__main__':
    aparser = atomicParser()
    #use default on main
    metadata_file = '/home/ubuntu/sp4.meta'
    jsonfile = open(metadata_file, 'rt')
    ## Read one line at a time to handle mal-formed lines
    jsonMsgs = []
    ctr = 0
    line = jsonfile.readline()
    jsonMsgs.append(json.loads(line))
    while line:
        try:
            line = jsonfile.readline()
            jsonMsgs.append(json.loads(line))
            ctr = ctr+1
        except Exception:
            print('**************', line, '**************')
    jsonfile.close()        
    for ji, jmsg in enumerate(jsonMsgs):
        if 'topic' in jmsg.keys():
            aparser.proc_msg_psim(jmsg['topic'], jmsg)

    msgs_per_ac = {k:len(aparser.ac_wrappers[k].messages) for k in aparser.ac_wrappers.keys()}
    print('messages per AC', msgs_per_ac)
