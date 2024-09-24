#!/usr/bin/env python

### does initialization of the knowledge structure
### object is instantiated in the agent looks for necessary mesages
### to set up template which will be updated with player-specific info
### can also be run on a metadata file (--msgfile) for testing outside of live play

import csv
import json
import sys
import copy
from live_utils import *
#from proc_knowledge_msgs import process_json_file

#### will need to be one object that we intantiate in atomic_parser
#### make_world_tree--no other messages will be processed until
#### groundtruth initialized: victims, gravel, markers, threatsigns, rooms

## first off when i victim is moved is should ALSO be moved in the template
## then when evac message comes thru it is MOVED for mover & template but REMOVED for al other players


class atomicParser(object): 
    def __init__(self):
        self.init_kstruct = {} # initial raw message for semantic map -- LIVE ONLY
        self.kstruct_template = make_regions() # this will be generic template player_kstructs will have player-specific info
        self.player_kstructs = [] # array of dicts, one for each player
        self.kset = False
        self.vmsg = {}
        self.vset = False
        self.rolestxt = {}
        self.rset = False
        self.gravelmsg = {}
        self.gset = False
        self.threatmsg = {}
        self.tset = False
        #self.reg_dicts = make_regions()
        # change to array of dicst that will have name:init_role
        self.players = []
        self.pset = False
        self.chat_msg = 'DEFAULT'
        self.critical_room = ''
        self.all_victims = []
        self.num_critical_victim_signals = 0
        self.rooms = []
        self.init_victims_placed = []
    # sets up map & creates template to be used for all players
    # which will list reg/rooms, victims, gravel, markers, threatsigs 
    # marked TRUE if player has seen or FALSE otherwise

    # for each init func calling, check what all is set & see if can complete template!!
    #             if kset and vset and rset and gset and tset:
    def load_semantic_map(self, rawmsg):
        self.kset = True
        #self.init_kstruct = json.loads(rawmsg)
        self.init_kstruct = rawmsg
        if self.kset and self.vset and self.rset and self.gset and self.tset and self.pset:
            self.generate_kstruct_template()
        return
    def add_victim_list(self, rawmsg):
        self.vset = True
        self.vmsg = rawmsg
        if self.kset and self.vset and self.rset and self.gset and self.tset and self.pset:
            self.generate_kstruct_template()
    # storing role txt
    # looks up which text should be associated with 
    # this player's selected role
    def add_role_txt(self, data):
        player = 'PLAYER_NOT_SET'
        pkstruct = {}
        for p in self.players:
            if data['playername'] == p['name']:
                player = p
        new_role = data['new_role']
        player['role'] = new_role        
        if new_role == 'Medical_Specialist':
            player['role'] = player['role']+", "+self.rolestxt['medical_specialist_text'][0]
        if new_role == 'Engineering_Specialist':
            player['role'] = player['role']+", "+self.rolestxt['engineering_specialist_text'][0]
            self.critical_room = self.rolestxt['engineering_specialist_text'][0].split("occurred in ")[1].strip().replace('.','')
        if new_role == 'Transport_Specialist':
            player['role'] = player['role']+", "+self.rolestxt['transport_specialist_text'][0]
            # eventually need to iter thru list? for now only one message is received

    def add_gravel_blockage_list(self, rawmsg):
        self.gset = True
        self.gravelmsg = rawmsg
        if self.kset and self.vset and self.rset and self.gset and self.tset and self.pset:
            self.generate_kstruct_template()
        return
    def add_threatsigns(self, rawmsg):
        self.tset = True
        self.threatmsg = rawmsg
        if self.kset and self.vset and self.rset and self.gset and self.tset and self.pset:
            self.generate_kstruct_template()
        return
    
    def get_playerlist(self, client_info_list):
        self.pset = True
        for p in client_info_list:
            pname = p['playername']
            prole = 'ROLE_NOT_SET'
            player = {'name':pname, 'role':prole}
            self.players.append(player)
        if self.kset and self.vset and self.rset and self.gset and self.tset and self.pset:
            self.generate_kstruct_template()

    def proc_msg(self, msgdict):
        # might need to pass msg AND data
        # do pre-proc (usually called in process_json_file)
        # comes in as dict so can use in live play
        # this should add a message to atomicparser.chat_msg that can be pushed to chat
        # regardless of player need to handle...change 'seen' to false if curr player & player doing the moving dont match
        # if don't wanna look for key, can just str it & keep line.find??
        line = str(msgdict)
        playername = 'PLAYER_NOT_SET'
        pkstruct = {}
        data = msgdict[u'data']
        for p in self.players:
            if line.find(p['name']) > -1:
                playername = p['name']
        # get kstruct for curr player
        for ks in self.player_kstructs:
            if ks['player'] == playername:
                pkstruct = ks

        # might need to swap msgdict for msgdict['data']??
        if line.find('VictimEvacuated') > -1 and line.find('mission_timer') > -1 and line.find('not initialized') == -1:
            move_victim(msgdict, playername, self.player_kstructs)

        elif line.find('not initialized') == -1 and line.find('mission_timer') > -1 and line.find(playername) > -1:
            if line.find('marker_placed') > -1:
                for pks in self.player_kstructs:
                    add_marker_placed(data,pkstruct,playername)

        # what room are we in, need to increment time
        x = 0
        z = 0
        #  determine region & room
        if 'x' in data.keys():
            x = data['x']
            z = data['z']
            reg = find_region(x,z,pkstruct) 
            rm = find_room(x,z,reg)

            if reg == 'NONE' or rm == 'NONE':
                pass # skip message if player is still at entrance & not in a proper room/region
            else:
                for v in rm['victims']:
                    v['seen'] = True
                    # determine gravel in room & mark as seen (will update to use proximity once decide how close)
                for gr in rm['gravel']:
                    gr['seen'] = True
                for ts in rm['threatsigns']:
                    ts['seen'] = True
                for m in rm['markers']:
                    m['seen'] = True

                if line.find('Critical Victim Detected') > -1 and line.find('Event:Signal') > -1: 
                    crit_vic_detected(pkstruct, rm)
                    self.num_critical_victim_signals += 1
    
    # need to separate generation of rooms & the adding of victims to rooms as the info arrives in sep msgs
    # won't have victim info when we receive semantic map init message
    # call this once we know we have vmsg, gravelmsg, etc
    def generate_kstruct_template(self):
        kstruct_temp = {}
        loc_list = self.init_kstruct['data']['semantic_map']['locations']
        num_locs = len(self.init_kstruct['data']['semantic_map']['locations'])
        loc_cnt = 0
        while loc_cnt < num_locs-1:
            k1 = loc_list[loc_cnt]
            if k1['type'] == 'treatment' or (k1['type'] == 'room' and 'child_locations' not in k1.keys()):
                k1['time_in'] = 0
                k1['victims'] = []
                k1['gravel'] = []
                k1['threatsigns'] = [] # skip for now freezeblock_list empty for s3 metadata
                k1['markers'] = []
                k1['critical_victim_detected'] = False
                coords = k1['bounds']['coordinates']
                rx0 = coords[0]['x']
                rz0 = coords[0]['z']
                rx1 = coords[1]['x']
                rz1 = coords[1]['z']

                rname_id = k1['id']
                # once room added to region in template, can then add the rest of the stuff to that room IN the template
                for rd in self.kstruct_template['reg_locations']: # determines which region this room_part is in
                    reg = region(rd)
                    if reg.in_region(rx0, rz0): #room pt is in reg, add to reg dict
                        rd['rooms'].append(k1)

                # SET VICTIMS TO SEEN IF ROOM NAME/ID MATCHES CRITICAL ROOM
                add_victims_to_room(k1, self.vmsg, self.kstruct_template, self.critical_room, self.init_victims_placed)
                add_gravel_to_room(k1, self.gravelmsg, self.kstruct_template)
                add_threatsigns_to_room(k1, self.threatmsg, self.kstruct_template)

            loc_cnt += 1
            # if it's a room & it DOES have child locations combine into parent room
            if k1['type'] == 'room' and 'child_locations' in k1.keys():
                sub_idx = loc_cnt # maybe don't need
                allxs = []
                allzs = []
                leftx = 0
                rightx = -3000
                topz = 100
                bottomz = -100
                nsubrooms = len(k1['child_locations'])
                for sidx in range(sub_idx, sub_idx+nsubrooms):
                    sk1 = loc_list[sidx]
                    coords = sk1['bounds']['coordinates']
                    allxs.append(coords[0]['x'])
                    allzs.append(coords[0]['z'])
                    allxs.append(coords[1]['x'])
                    allzs.append(coords[1]['z'])
                    loc_cnt += 1
                leftx = sorted(allxs)[0]
                topz = sorted(allzs)[0]
                rightx = sorted(allxs)[len(allxs)-1]
                bottomz = sorted(allzs)[len(allzs)-1]
                # make & append room here!! with leftx,miny X rightx, maxy
                # keep last assigned sk1 & update with coords, etc
                sk1['time_in'] = 0
                sk1['victims'] = []
                sk1['gravel'] = []
                sk1['threatsigns'] = [] # skip for now freezeblock_list empty for s3 metadata
                sk1['markers'] = []
                sk1['critical_victim_detected'] = False
                sk1['bounds']['coordinates'][0]['x'] = leftx
                sk1['bounds']['coordinates'][0]['z'] = topz
                sk1['bounds']['coordinates'][1]['x'] = rightx
                sk1['bounds']['coordinates'][1]['z'] = bottomz
                sk1['type'] = 'room'
                sk1['name'] = sk1['name'].replace('Part of ','')
                # split to parent name for assignment
                sk1['id'] = sk1['id'].split('_')[0]
                # now have merged room from subparts, do all steps did for regular rooms---can steps be combined?
                self.rooms.append(room(sk1)) 
                add_victims_to_room(sk1, self.vmsg, self.kstruct_template, self.critical_room, self.init_victims_placed)
                add_gravel_to_room(sk1, self.gravelmsg, self.kstruct_template)
                add_threatsigns_to_room(sk1, self.threatmsg, self.kstruct_template)
                for rd in self.kstruct_template['reg_locations']: # determines which region this room_part is in--CHCK WHICH ROOMS GO IN REG
                    reg = region(rd)
                    if reg.in_region(leftx, topz): # merged room is in reg, add to reg dict
                        rd['rooms'].append(sk1)

        for conn in self.init_kstruct['data']['semantic_map']['connections']: #add all portals (spans multiple regions/rooms)
            self.kstruct_template['connections'].append(conn)

        # FOR DEBUGGING WRITE OUT KSTRUCT TEMPLATE (which is the initial struct for each player)
        tfile = open("saturn_template", 'w') 
        json.dump(self.kstruct_template, tfile ,indent=True)
        print("WROTE OUT TEMPLATE-----")
        ## add a kstruct for each player, include name
        do_add = True
        for p in self.players:
            # check not already added (should not have to add this!)
            for pks in self.player_kstructs:
                if p['name'] == pks['player']:
                    do_add = False
            # add palyername to self.kstruct/template
            # then add that to player kstruct array
            if do_add:
                player_kstruct = copy.deepcopy(self.kstruct_template) # do we need deep copy here????--might not matter
                player_kstruct.update({"player":p['name']})
                player_kstruct.update({"roles":p['role']})
                self.player_kstructs.append(player_kstruct)

######## for local testing
### should simulate funcs from atomic_parser

if __name__ == '__main__':        
    aparser = atomicParser()
    metadata_file = 'data/sp4_test.meta'
    
    # for testing with existing metadata file
    time_of_interest = 900000
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '--msgfile':
            metadata_file = sys.argv[i+1]
        elif sys.argv[i] == '--time-ms':
            time_of_interest = int(sys.argv[i+1])

    jsonfile = open(metadata_file, 'rt')

    # this should mimic what is called in atomic_parser/subscriptions
    # line.find should include what's on the subscription
    for line in jsonfile.readlines():
        if line.find('SemanticMap:Initialized') > -1 and line.find('locations') > -1 and not aparser.kset:
            aparser.load_semantic_map(line)
        elif line.find('client_info') > -1 and (not aparser.pset):
            jmsg = json.loads(line)
            aparser.get_playerlist(jmsg[u'data']['client_info'])
        elif line.find('mission_victim_list') > -1:
            aparser.add_victim_list(line)
        elif line.find('Mission:RoleText') > -1 and not aparser.rset and line.find('Event:RoleSelected') == -1: 
            aparser.rset = True
            aparser.rolestxt = json.loads(line)['data']
        elif line.find('role_selected') > -1 and line.find('playername') > -1:
            aparser.add_role_txt(json.loads(line)['data'])
        elif line.find('ground_truth/mission/blockages_list') > -1 and line.find('subscribes') == -1 and not aparser.gset:
            aparser.add_gravel_blockage_list(line)
        #elif line.find('mission_threatsign_list') > -1 and not aparser.tset:
        elif line.find('ground_truth/mission/threatsign_list') > -1 and line.find('subscribes') == -1 and not aparser.tset:
            aparser.add_threatsigns(line)
        else:
            # all kstructs initiated can now proc any other types of msgs we're subscribed to
            if aparser.kset and aparser.vset and aparser.rset and aparser.gset and aparser.tset and aparser.pset and line.find('playername') > -1:
                aparser.proc_msg(json.loads(line))
    for kstruct in aparser.player_kstructs:
        print("stats for "+kstruct['player']+" ::")
        print("roles:: "+str(kstruct['roles']))
        victims = sorted(check_victims_seen(kstruct))
        print("victims seen:: "+str(victims))
        gravel = check_gravel_seen(kstruct)
        print("gravel seen:: "+str(gravel))
        markers = check_markers_seen(kstruct)
        print("markers seen:: "+str(markers))
        threatsigns = check_threatsigns_seen(kstruct)
        print("threat signs seen:: "+str(threatsigns)+"\n")
    print("total critical victim signals:: "+str(aparser.num_critical_victim_signals))
        
    # TODO: add func to write out each player's kstruct
    jsonfile.close()
    for pks in aparser.player_kstructs:
        pfile = open(pks['player'], 'w')
        json.dump(pks, pfile,indent=True)
        pfile.close()
    # use for launching processing when running live
    #aparser.post_processing()
    # example push stats to players
    print("chat msg == "+str(aparser.chat_msg))   
