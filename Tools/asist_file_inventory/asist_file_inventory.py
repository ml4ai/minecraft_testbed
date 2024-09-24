# Purpose: Takes a ls (not ls -l) of filenames and a standard for number of filename parts (e.g., 8 parts) separated by "_". Reports (1) team, trial, and count of each filetype, as well as (2) filenames that do not conform to the standard of number of parts
# Author: Jared Freeman
# Date: 11/13/21
# Use: python asist_file_inventory.py 8 2 log1.txt >inventory.txt
# Dependencies:
	# ls as input
	# filenames that largely conform to the Study-2 syntax 
	# filepart count

# v4 = Revised command line handling to accept the in and out files in OS independent manner (i.e., only the integer parameters are required)

# To Do
	# Revise the next generation of filenames to ensure that the format is Trial- Team- Member- (in whatever order). See "parttrial = fileparts" for explanation
	# Consider whether to change this too-long filename in GCS of this?: 'HSRData', 'Surveys0Fulltext', 'Trial-na', 'Team-na', 'Member-na', 'CondBtwn-na', 'CondWin-na', 'HumanAdvisor', 'Vers-1.csv'

import sys

#########################
# Validate command line parameters & convert to variables OR issue help and exit(). Set up other variables
helpme = "This script takes a ls of ASIST data files as input and generates an report inventory.txt.\nUse: python asist_file_inventory.py filepartcount fileparttype inputfile >outputfile\n     filepartcount is an integer indicating the number of _ separated tokens in a canonical filename\n     fileparttype is an integer indicating the token that indicates the type of file (trialmessages, OBVideo, etc."
if (len(sys.argv) <= 2):
  print ("You called this script with too few parameters on the command line. Read instructions:\n",helpme)
try:
  filepartcount = int(sys.argv[1])
except: 
  print ("You entered a non-integer parameter after the script name. Read instructins:\n",helpme)
try:
  fileparttype = int(sys.argv[2])-1
except: 
  print ("You entered a non-integer parameter after the script name. Read instructins:\n",helpme)

fileinput = (sys.argv[3])
f = open(fileinput, "r")
nonconformantnames = []
surveynames = []
typelist = []
partdict = {}

#########################
# Parse the input ls file and populate variables 
for line in f:
  # Prep line by stripping off path and \n, then splitting filename on "_" into its parts  
  #print(line)
  line = line.rstrip()
  filename = line.split("/")
  #print(filename)
  x = len(filename)-1
  fileparts = filename[x].split("_")

  # Handle filenames with too few or many parts
  #if len(fileparts) != filepartcount:
  if len(fileparts) < filepartcount:
    nonconformantnames.append(filename[x])
    continue
  # Parse filenames that conform to type_trial_team_member format
  #print(fileparts)
  ####parttype = fileparts[1]
  parttype = fileparts[fileparttype]
  #cprint ("parttype=",parttype)
  
  if parttype.find("Survey") != -1:
    #print ("HIT ---> ", parttype)
    surveynames.append(parttype)
    continue
  
  #parttrial = fileparts[2]
  # We're forced to use the "or" construction because we must catch file names Trial- and TrialPlanning
    # "[s...Trial..." fails bcs it interprets TrialMessages (and other components that precede Trial) to be the Trial when in fact it is the type
    # "[s...Trial-..." fails bcs "TrialPlanning" filenames do not contain "Trial-", and this throws an error.
  parttrial = [s for s in fileparts if "Trial-" in s] or [s for s in fileparts if "TrialPlanning" in s]
  parttrial = parttrial[0] 
  partteam = [s for s in fileparts if "Team" in s]
  partteam = partteam[0]
  partmember = [s for s in fileparts if "Member" in s]
  partmember = partmember[0]
  
  # Compile a list of unique file parttypes (e.g., ZoomAudio)
  if not(parttype in typelist):
    typelist.append(parttype)
  # Create a dictionary of key=partteam+parttrial+parttype, value=count
  ptt = partteam+"_"+partmember+"_"+parttrial
  #print(ptt)
  if ptt in partdict:
    partdict[ptt].append(parttype)
  else: 
    partdict[ptt]=[parttype]

f.close()
#print(partdict)
#print(typelist)
#print(surveynames)

#########################
# Print report

print ("Non-conformant filenames")
print ("Note: These files have names that do not conform to the typical filename structure, either by design or by accident. Most concern all Teams, Members and Trials in the study, not one.")
for n in nonconformantnames:
  print (n)

print ("\nSurvey filenames")
print ("Note: These files contain survey data, typically for all Teams, Members and Trials in the study, not one.")
for s in surveynames:
  print (s)

print ("\nConformant filenames")
print ("Note: These files concern a specific Team, team Member, or Trial in the study. Their file names conform to the typical filename structure.")
header = "Team\tMember\tTrial\t"
for t in typelist:
  header += t
  header += "\t"

print (header)
for p in partdict:
  #print (p)
  row = ""
  team,member,trial = p.split("_")
  row += team
  row += "\t"
  row += member
  row += "\t"
  row += trial
  row += "\t"
  for t in typelist:
    #print (t)
    ct = partdict[p].count(t)
    row += str(ct)
    row += "\t"
  print (row)



