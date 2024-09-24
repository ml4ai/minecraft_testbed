#!/usr/bin/env python3

import csv
import json
import sys
#from proc_knowledge_msgs import *

# only adding room PARTS to regions...coords for parent rooms not in orig saturn file
# can map back to parent room during processing if needed?
class region(object):
    def __init__(self, rdict):
        self.name = rdict['id']
        x0 = rdict['x0']
        x1 = rdict['x1']
        z0 = rdict['z0']
        z1 = rdict['z1']
        self.x0= min(x0, x1)
        self.x1= max(x0, x1)
        self.z0= min(z0, z1)
        self.z1= max(z0, z1)
        self.rdict = rdict

    def in_region(self, _x, _z, epsilon = .5):
        return (self.x0 - epsilon <= _x) and (_x <= self.x1 + epsilon) and (self.z0 - epsilon <= _z) and (_z <= self.z1 + epsilon)
    
    def __repr__(self):
        return '%s %.0f %.0f %.0f %.0f' % (self.name, self.x0, self.x1, self.z0, self.z1)

class room(object):
    def __init__(self, rdict):
        self.name = rdict['id']
        x0 = rdict['bounds']['coordinates'][0]['x']
        x1 = rdict['bounds']['coordinates'][1]['x']
        z0 = rdict['bounds']['coordinates'][0]['z']
        z1 = rdict['bounds']['coordinates'][1]['z']
        self.x0= min(x0, x1)
        self.x1= max(x0, x1)
        self.z0= min(z0, z1)
        self.z1= max(z0, z1)
        self.rdict = rdict

    def in_room(self, _x, _z, epsilon = 2): # increasing eps so critical signal associated with proper room
        return (self.x0 - epsilon <= _x) and (_x <= self.x1 + epsilon) and (self.z0 - epsilon <= _z) and (_z <= self.z1 + epsilon)
    
    def __repr__(self):
        return '%s %.0f %.0f %.0f %.0f' % (self.name, self.x0, self.x1, self.z0, self.z1) 

class victim(object):
    def __init__(self, x, z, vid, rm=''):
        self.rm = rm
        self.vid = vid
        self.x = x
        self.z = z
        

# set room here get rid of sep func for getting curr room
# only need one kstruct, vic will be in same
# room for all players, will just have diff 
# 'seen' status
def find_vic_curr_vdict(vid, kstruct):
    curr_vdict = {}
    for region in kstruct['reg_locations']:
        for rm in region['rooms']:
            r = room(rm)
            for v in rm['victims']:
                if v['unique_id'] == vid:
                    v['setlocation'] = r.name
                    curr_vdict = v
    return curr_vdict

# should not have to iter?
def crit_vic_detected(pkstruct, curr_room):
    crit_room = False
    for region in pkstruct['reg_locations']:
        for rm in region['rooms']:
            #r = room(rm)
            if rm['id'] == curr_room['id']:
                rm['critical_victim_detected'] = True

#### SHOULD I MOVE THE VICTIM IN THE TEMPLATE SO HAVE REFERENCE??

def find_vic_new_room(nx, nz, kstruct):
    rname = 'NONE'
    for region in kstruct['reg_locations']:
        for rm in region['rooms']:
            r = room(rm)
            if r.in_room(nx,nz):
                rname = r.name
    return rname


    def find_new_room(self,vid,x,z,kstruct):
        for region in self.kstruct['reg_locations']:
            for rm in region['rooms']:
                r = room(rm)
                if r.in_room(x,z): # we know this is the new rrom we ant to add this vic to
                    return r.name
        return 'NONE'

#TODO: if victim is in initial casualty room MARK AS SEEN
# rdict/k1 starts off with no victims we add the ones created
# that fall in the realm of this "location"
def add_victims_to_room(rdict,raw_vmsg, kstruct_template, croom, init_placed_vid_list):
    vmsg = raw_vmsg['data']['mission_victim_list']
    vroom = room(rdict)
    for victim in vmsg:
        vic_rm_found = False
        vx = victim['x']
        vz = victim['z']
        vid = victim['unique_id']
        if vroom.in_room(vx,vz,.5) and vid not in init_placed_vid_list: # victim is in this room & not already assigned
            # CHECK IF FROM INITIAL blast
            new_victim = {}
            new_victim['unique_id'] = vid
            new_victim['block_type'] = victim['block_type']
            new_victim['room_name'] = vroom.name
            new_victim['seen'] = False # default to false, set below if we're in croom
            if croom == new_victim['room_name']: # this is critical init room
                new_victim['seen'] = True
                # skipping check if has setlocation JUST REASSIGN----maybe don't need....just add to kstruct_temp
            rdict['victims'].append(new_victim)
            init_placed_vid_list.append(vid)
  
#------error checking
def check_victims_assigned(raw_vmsg):
    vmsg = raw_vmsg['data']['mission_victim_list']
    for v in vmsg:
        if not 'setlocation' in v.keys():
            print("VICTIM NOT IN ROOM....."+str(v))

# if rooms match don't need to swap just update coords
# add breaks/pass room name to speed up?
# skip if NONE
def update_victim_coords(nx, nz, allkstructs, vdict):
    vid = vdict['unique_id']
    for kstruct in allkstructs:
        for region in kstruct['reg_locations']:
            for rm in region['rooms']:
                for v in rm['victims']:
                    if v['unique_id'] == vid: 
                        v['x'] = nx # use update instead?
                        v['z'] = nz
                break # don't check rest of rooms since found vic room

# runs for each player kstruct if seen == false means curr player not the one moving it
def swap_room_victim(vid, curr_rm, new_rm, nx, nz, pkstruct, vdict, seen):
    old_room_new_vlist = []
    new_room_new_vlist = []
    # go thru existing struct & remove vic from curr_room (meaning old_room_new_vlist should not have this victim in it)
    for region in pkstruct['reg_locations']:
        for rm in region['rooms']:
            if rm['id'] == curr_rm: # this is where victim is now. so, add all victims EXCEPT this one to the new vlist for this room
                for v in rm['victims']:
                    if v['unique_id'] != vid: 
                        old_room_new_vlist.append(v)
                rm['victims'] = old_room_new_vlist
 
    # make new one & append to new room vic list
    # TODO: check SEEN
    vdict = {'z':nz, 'block_type':vdict['block_type'], 'x': nx,'y':60,'unique_id':vid, 'seen':seen, 'setlocation':vdict['setlocation']}
    new_loc = 'NONE'
    for region in pkstruct['reg_locations']:
        for rm in region['rooms']:
            if rm['id'] == new_rm: # add newly created victim to this room as well as it's existing victims
                new_loc = new_rm
                vdict['setlocation'] = new_rm
                rm['victims'].append(vdict) 
            # we've added victim to new room need to make sure update old room list
            elif rm['id'] == curr_rm: # old room here
                rm['victims'] = old_room_new_vlist
    #print("====== moved vic, victims seen for
    vdict['setlocation'] = new_loc # tracking 'NONE' for error checking
                
def print_victims_info(kstruct):
    print("FULL VICTIM LOCATIONS.................")
    for region in kstruct['reg_locations']:
        for rm in region['rooms']:
            print("ROOM "+str(rm['id'])+" has "+str(len(rm['victims'])))
            for v in rm['victims']:
                print(str(v['unique_id'])+" ,")

def add_victims_to_list():
    fullvdict_data = self.messages[1]['data']
    vlist = []
    for v in self.victims:
        vic_type = 'block_victim_2'
        if v[2].find('g') > -1:
            vic_type = 'block_victim_1'
        vdict = {'z':v[1], 'block_type':vic_type, 'x': v[0],'y':60,'victim_id':v[2]}
        vlist.append(vdict)
        fullvdict_data.update({"mission_victim_list":vlist})

def add_gravel_to_room(rdict, gravelmsg, kstruct_template):
    gravel_cnt = 0 # use for adding id's may not work since later rubble msgs won't have id
    groom = room(rdict)
    rdict['gravel'] = []
    for gdict in gravelmsg['data']['mission_blockage_list']:
        if gdict['block_type'] == 'gravel' and gdict['feature_type'] == 'obstruction':
            gx = gdict['x']
            gz = gdict['z']
            if groom.in_room(gx, gz):
                if gdict['room_name'] == 'NA': #if room not yet set for this
                    gdict['room_name'] = groom.name
                    rdict['gravel'].append(gdict)
                    gravel_cnt += 1
                    gdict.update({'seen':True})
                    gdict.update({'id':str(gravel_cnt)+groom.name})

def add_threatsigns_to_room(rdict, threatmsg, kstruct_template):
    threatsign_cnt = 0 # use for adding id's may not work since later rubble msgs won't have id
    troom = room(rdict)
    rdict['threatsigns'] = []
    for tdict in threatmsg['data']['mission_threatsign_list']:
        if tdict['block_type'] == 'block_rubble_collapse':
            tx = tdict['x']
            tz = tdict['z']
            if troom.in_room(tx, tz):
                if tdict['room_name'] == 'NA': #if room not yet set for this
                    tdict['room_name'] = troom.name
                    rdict['threatsigns'].append(tdict)
                    threatsign_cnt += 1
                    tdict.update({'seen':True})
                    tdict.update({'id':str(threatsign_cnt)+troom.name})

def check_victims_seen(kstruct):
    vicstats = []
    for (k,val) in kstruct.items():
        if k == 'reg_locations':
            for r in val:
                rooms = r['rooms']
                for rm in rooms:
                    victims = rm['victims']
                    for v in victims:
                        if v['unique_id'] in vicstats: # only for error checking
                            print("WE HAVE A DUP VICTIM SEEN....."+str(v['unique_id']))
                        if v['seen']: 
                            vicstats.append(v['unique_id'])
    return vicstats

# if victim is being moved must change its room assignment
# & change it to seen = FALSE if curr player is NOT the one moving it (later will need to include proximity check)
# have full kstruct here, so change loc of vic for all players?? (maybe not, maybe just curr player)
# MIGHT BE JUST COMING IN AS 'DATA' , don't need to reference out
def move_victim(fullmsg, playername ,allkstructs):
    data = fullmsg[u'data']
    am_moving = False
    kstruct = {}
    # change room/reg vic is associated with & set seen to false UNLESS we are the one moving it
    vid = data['victim_id']
    for ks in allkstructs:
        if ks['player'] == playername:
            kstruct = ks

    new_x = data['victim_x']
    new_z = data['victim_z']
    curr_room_name = 'NONE'
    # only need one kstruct, vic will be in same
    # room for all players, will just have diff 
    curr_vdict = find_vic_curr_vdict(vid,kstruct)
    if not curr_vdict: 
        print("CAN'T FIND ROOM FOR VICTIM:: "+str(vid)+" fullmsg == "+str(fullmsg))
        #print("line = "+str(line))
    else:
        curr_room_name = curr_vdict['setlocation']
        new_room_name = find_vic_new_room(new_x, new_z, kstruct)
        #print("_____MOVING VICTIM____ player = "+str(playername)+" ==>> "+str(vid)+" from room "+str(curr_room_name)+" TO "+str(new_room_name))
        if curr_room_name == new_room_name and curr_room_name != 'NONE':
            # player has not changed rooms but has new coords
            # will need to update for each player kstruct
            update_victim_coords(new_x, new_z, allkstructs, curr_vdict)
        else:
            # swap room for each player, seen only true for player in curr moving message
            for pk in allkstructs:
                if pk['player'] == playername:
                    am_moving = True
                swap_room_victim(vid,curr_room_name, new_room_name, new_x, new_z, pk, curr_vdict, am_moving)

def check_moved_victim_seen(kstruct, victim): #need player?
    vicstats = []
    for (k,val) in kstruct.items():
        if k == 'reg_locations':
            for r in val:
                rooms = r['rooms']
                for rm in rooms:
                    victims = rm['victims']
                    for v in victims:
                        if v['seen']:
                            vicstats.append(v['id'])
    return vicstats

def check_gravel_seen(kstruct):
    gravstats = []
    for region in kstruct['reg_locations']:
        rooms = region['rooms']
        for rm in rooms:
            gravel = rm['gravel']
            for rb in gravel:
                if rb['seen'] and rb['id'] not in gravstats:
                    gravstats.append(rb['id'])
    return gravstats

def check_threatsigns_seen(kstruct):
    threatstats = []
    for region in kstruct['reg_locations']:
        rooms = region['rooms']
        for rm in rooms:
            threatsigns = rm['threatsigns']
            for ts in threatsigns:
                if ts['seen'] and ts['id'] not in threatstats:
                    threatstats.append(ts['id'])
    return threatstats

def add_marker_placed(data,kstruct,curr_player):
    mx = data['marker_x']
    mz = data['marker_z']
    seen = False
    player_placing = data['playername']
    if player_placing == curr_player:
        seen = True
    regions = kstruct['reg_locations']
    for r in regions:
        rooms = r['rooms']
        for rm in rooms:
            rmobj = room(rm)
            if rmobj.in_room(mx,mz):
                mkrdict = {"x":mx,"z":mz,"seen":seen}
                if mkrdict not in rm['markers']:
                    rm['markers'].append(mkrdict)

def check_markers_seen(kstruct):
    mstats = []
    regions = kstruct['reg_locations']
    for r in regions:
        rooms = r['rooms']
        for rm in rooms:
            markers = rm['markers']
            for m in markers:
                mcoords = (m['x'],m['z'])
                if m['seen'] and mcoords not in mstats:
                    mstats.append(mcoords)
    return mstats

# altering nik's orig coords so lower bound includes all of safe zones
def make_regions():
    reg_dicts = {}
    reg_dicts['roles'] = []
    reg_dicts['reg_locations'] = []
    reg_dicts['connections'] = []

    reg_dict1 = {"id": "reg_1",
                 "type": "region",
                 "x0": -2225,
                 "z0": -11,
                 "x1": -2175,
                 "z1": 26,
                 "time_in": 0,
                 "rooms":[]
                 }
    reg_dict2 = {"id": "reg_2",
                 "type": "region",
                 "x0": -2225,
                 "z0": 27,
                 "x1": -2175,
                 "z1": 64,
                 "time_in": 0,
                 "rooms":[]
                 }
    reg_dict3 = {"id": "reg_3",
                 "type": "region",
                 "x0": -2174,
                 "z0": -11,
                 "x1": -2135,
                 "z1": 26,
                 "time_in": 0,
                 "rooms":[]
                 }
    reg_dict4 = {"id": "reg_4",
                 "type": "region",
                 "x0": -2174,
                 "z0": 27,
                 "x1": -2135,
                 "z1": 64,
                 "time_in": 0,
                 "rooms":[]
                 }
    reg_dict5 = {"id": "reg_5",
                 "type": "region",
                 "x0": -2134,
                 "z0": -11,
                 "x1": -2087,
                 "z1": 26,
                 "time_in": 0,
                 "rooms":[]
                 }
    reg_dict6 = {"id": "reg_6",
                 "type": "region",
                 "x0": -2134,
                 "z0": 27,
                 "x1": -2087,
                 "z1": 64,
                 "time_in": 0,
                 "rooms":[]
                 }

    reg_dicts['reg_locations'].append(reg_dict1)
    reg_dicts['reg_locations'].append(reg_dict2)
    reg_dicts['reg_locations'].append(reg_dict3)
    reg_dicts['reg_locations'].append(reg_dict4)
    reg_dicts['reg_locations'].append(reg_dict5)
    reg_dicts['reg_locations'].append(reg_dict6)
    return reg_dicts
    
def get_players(fname):
    players = []
    jsonfile = open(fname, 'rt')
    for line in jsonfile.readlines():
        if line.find('playername') > -1:
            jmsg = json.loads(line)
            data = jmsg[u'data']
            playerlist = data['client_info']
            for pdict in playerlist:
                players.append(pdict['playername'])
            jsonfile.close()
            break
    return players

# find reg & increment time
def find_region(x,z,kstruct):
    for (k,v) in kstruct.items():
        if k == 'reg_locations':
            for r in v:
                reg = region(r)
                # check if in region
                inreg = reg.in_region(x,z)
                if inreg:
                    reg.rdict['time_in'] += 1
                    return reg.rdict
    return "NONE"

def find_room(x,z,region):
    if region == 'NONE':
        pass
    else:
        for rdict in region['rooms']:
            r = room(rdict)
            if r.in_room(x,z):
                rdict['time_in'] += 1
                return rdict
        return "NONE"
