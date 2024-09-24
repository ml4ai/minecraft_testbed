import docker
import os
import subprocess
import sys
import time
import argparse

client = docker.from_env()
root_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
os_type = sys.platform
slash = '/'
if os_type == 'win32':
    slash = '\\'

print('Bring down MQTT')
dir = root_dir + slash + 'mqtt'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down ELK')
dir = root_dir + slash + 'ELK-Container'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down metadata server')
dir = root_dir + slash + 'metadata' + slash + 'metadata-docker'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down export/import dashboard')
dir = root_dir + slash + 'metadata' + slash + 'metadata-web'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down AC_IHMC_TA2_Location-Monitor Agent')
dir = root_dir + slash + 'Agents' + slash + 'AC_IHMC_TA2_Location-Monitor'
os.chdir(dir)
subprocess.run(['docker-compose', '--env-file', 'settings.env', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down AC_IHMC_TA2_Player-Proximity Agent')
dir = root_dir + slash + 'Agents' + slash + 'AC_IHMC_TA2_Player-Proximity'
os.chdir(dir)
subprocess.run(['docker-compose', '--env-file', 'settings.env', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down AC_IHMC_TA2_Dyad-Reporting Agent')
dir = root_dir + slash + 'Agents' + slash + 'AC_IHMC_TA2_Dyad-Reporting'
os.chdir(dir)
subprocess.run(['docker-compose', '--env-file', 'settings.env', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down AC_IHMC_TA2_Joint-Activity-Interdependence Agent')
dir = root_dir + slash + 'Agents' + slash + 'AC_IHMC_TA2_Joint-Activity-Interdependence'
os.chdir(dir)
subprocess.run(['docker-compose', '--env-file', 'settings.env', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down AC_CMUFMS_TA2_Cognitive Agent')
dir = root_dir + slash + 'Agents' + slash + 'AC_CMUFMS_TA2_Cognitive'
os.chdir(dir)
subprocess.run(['docker-compose', '--env-file', 'settings.env', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down CMU TA2 Team Effectiveness Diagnostic AC')
dir = root_dir + slash + 'Agents' + slash + 'AC_CMU_TA2_TED'
os.chdir(dir)
subprocess.run(['docker-compose', '--env-file', 'settings.env', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down CMU TA2 BEARD AC')
dir = root_dir + slash + 'Agents' + slash + 'AC_CMU_TA2_BEARD'
os.chdir(dir)
subprocess.run(['docker-compose', '--env-file', 'settings.env', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down AC_CMU_TA1_PyGLFoV Agent')
dir = root_dir + slash + 'Agents' + slash + 'AC_CMU_TA1_PyGLFoVAgent'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down the SIFT Asistant Agent')
dir = root_dir + slash + 'Agents' + slash + 'SIFT_Asistant_Agent'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down the CMU-TA1 ATLAS Agent')
dir = root_dir + slash + 'Agents' + slash + 'ASI_CMU_TA1_ATLAS'
os.chdir(dir)
subprocess.run(['docker-compose', '--env-file', 'settings.env', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down the Cornell Team Trust AC')
dir = root_dir + slash + 'Agents' + slash + 'ac_cornell_ta2_teamtrust'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down Gallup Agent GELP')
dir = root_dir + slash + 'Agents' + slash + 'gallup_agent_gelp'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down Gallup Agent GOLD')
dir = root_dir + slash + 'Agents' + slash + 'gallup_agent_gold'
os.chdir(dir)
subprocess.run(['docker-compose', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Bring down Minecraft')
dir = root_dir + slash + 'Local'
os.chdir(dir)
subprocess.run(['docker-compose', '-f', 'docker-compose.asistmod.yml', 'down', '--remove-orphans'])
os.chdir(root_dir)

print('Testbed stopped')

client.close()
