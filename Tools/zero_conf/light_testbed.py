#!/usr/bin/env python3
#
# Copyright (c) 2020 SIFT
#
"""
Script to launch just the testbed components we need.
"""

import argparse
import os
import subprocess
import sys
import platform

import paho.mqtt.client as mqtt


def main(args):
    """Main entry point for script."""
    parser = argparse.ArgumentParser(description=__doc__)
    config = parser.parse_args(args)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config.testbed_dir = os.path.join(script_dir, '..', '..')

    config.mqtt_host = 'localhost'

    if not os.path.exists(config.testbed_dir):
        raise ValueError(f'Testbed directory does not exist: {config.testbed_dir}')

    ensure_mqtt(config)

    # Start IHMC location monitor.
    ensure_location_monitor(config)

    # Start ELK
    ensure_elk(config)

    # Start CU_request_tracker
    ensure_request_tracker(config)

    # Reset the server (map) data. This is normally done when you click "stop
    # mission" in the MalmoControl interface. The relevant code is in
    # MalmoControl/Controllers/ExperimentController.cs -- look for
    # deleteMapCommand and copyMapCommand. But we want to do it before starting
    # up so that we have a clean world for each pass.
    #
    # reset_minecraft_map_data('Saturn_1.6_3D', config)
    reset_minecraft_map_data('Saturn_2.0_3D', config)

    # Bring up Minecraft.
    ensure_minecraft(config)


def ensure_mqtt(config):
    """
    Makes sure the MQTT bus docker container is running.
    """
    print('Making sure Mosquitto bus is running')
    docker_compose_up('mqtt', config)

    # Make sure we can connect to MQTT. connect() is a blocking function, so
    # once this succeeds, we can proceed.

    client = mqtt.Client(userdata=config)
    mqtt_port = 1883
    print(f'Connecting to MQTT at: {config.mqtt_host}:{mqtt_port}')
    client.connect(config.mqtt_host, mqtt_port, 60)

    # We may consider publishing a hello message to confirm that the bus is
    # operational. But for now, let's skip it.
    print('  Success, moving on.')


def ensure_location_monitor(config):
    """
    Makes sure the IHMC Location Monitor docker container is running.
    """
    print('Making sure IHMC Location Monitor is running')
    docker_compose_up(os.path.join('Agents', 'IHMCLocationMonitor'),
                      config,
                      env_filename='settings.env')

def ensure_request_tracker(config):
    """
    Makes sure the Cornell Request Tracker docker container is running.
    """
    print('Making sure Cornell Request Tracker is running')
    docker_compose_up(os.path.join('Agents', 'cu_request_ac'),
                      config,
                      env_filename='settings.env')

def ensure_elk(config):
    """
    Makes sure the ELK docker container is running.
    """
    print('Making sure ELK is running')
    docker_compose_up('ELK-Container', config)


def reset_minecraft_map_data(map_name, config):
    """
    Resets the Minecraft server's map data to the fresh state.
    """
    ensure_minecraft_data_dir(config)

    local_dir = os.path.relpath(os.path.join(config.testbed_dir, 'Local'))

    cleanmaps_dir = os.path.join(local_dir, 'CLEAN_MAPS')
    cleanmap_dir = os.path.join(cleanmaps_dir, map_name)

    minecraft_data_dir = os.path.join(local_dir, 'MinecraftServer', 'data')
    minecraft_map_dir = os.path.join(minecraft_data_dir, map_name)

    print('Copying clean map data from:')
    print(f'  {cleanmap_dir}')
    print('To Minecraft server data directory:')
    print(f'  {minecraft_map_dir}')

    # We remove and copy the files using shell commands because it was harder to
    # do with Python commands (e.g., shutil). If we remove or replace the data
    # directory itself (rather than its contents), we damage the Minecraft
    # server's ability to start up (unless we restart docker first!).
    _delete(minecraft_map_dir)
    _copy(cleanmap_dir, minecraft_map_dir)

    # We also need to rewrite the level-name value in the server properties file
    # so that the server loads the correct map.
    server_properties_file = \
        os.path.join(minecraft_data_dir, 'server.properties')
    print(f'Rewriting level-name in: {server_properties_file}')
    lines = []
    with open(server_properties_file, 'rt') as in_file:
        for line in in_file:
            if line.startswith('level-name='):
                line = f'level-name={map_name}\n'
            lines.append(line)
    with open(server_properties_file, 'wt') as out_file:
        for line in lines:
            out_file.write(line)


def ensure_minecraft_data_dir(config):
    """
    Makes sure that the data have been copied -- at least once. Note that if we
    replace this directory while the minecraft server docker container is
    running, it will damage the functioning of that container.
    """
    local_dir = os.path.relpath(os.path.join(config.testbed_dir, 'Local'))
    minecraft_dir = os.path.join(local_dir, 'MinecraftServer')

    # If the minecraft directory does not already exist, make it now.
    if not os.path.exists(minecraft_dir):
        os.makedirs(minecraft_dir)

    data_dir = os.path.join(local_dir, 'data')
    minecraft_data_dir = os.path.join(minecraft_dir, 'data')
    _copy(data_dir, minecraft_data_dir)


def ensure_minecraft(config):
    """
    Makes sure the Minecraft server (and control panel) are up and running.
    """
    # The testbed_up script mucks about with the version in the MalmoControl
    # appsettings json file. We don't bother with that for local testing.

    # And the testbed_up script runs docker compose with sudo. We omit that
    # here, and it seems fine.
    orig_dir = os.getcwd()

    loc_dir = os.path.join(config.testbed_dir, 'Local')
    print(f'Running docker-compose in: {loc_dir}')
    os.chdir(loc_dir)

    # We do not need to check if the contains is already running. If it is, the
    # docker-compose command will just exit successfully.
    cmd = [
        # 'echo',
        'docker-compose',
        '-f', 'docker-compose.asistmod.yml',
        # '-f', 'docker-compose.minecraft.yml',
        'up',
        # Only start the Minecraft service.
        'minecraft'
        # This is optional. If we use this argument, the Minecraft docker
        # container runs in daemon mode (i.e., in the background). If we use it
        # here, our script will continue on and exit.
        #
        # For our local testing, it is more useful to keep it in the foreground
        # so that we can watch the messages on the server. It helps us spot
        # errors.
        #
        # But it also makes this a blocking call. So we may not always be able
        # to do this.
        #
        # '-d'
    ]
    subprocess.run(cmd, check=True)

    # All done, go back to original working dir.
    os.chdir(orig_dir)


def docker_compose_up(compose_dir, config, env_filename=None):
    """
    Goes to the directory in question and runs docker-compose up. The
    compose_dir should be relative to the testbed root.
    """
    orig_dir = os.getcwd()

    loc_dir = os.path.join(config.testbed_dir, compose_dir)
    print(f'Running docker-compose in: {loc_dir}')
    os.chdir(loc_dir)

    # We do not need to check if the contains is already running. If it is, the
    # docker-compose command will just exit successfully.
    cmd = [
        # 'echo',
        'docker-compose',
    ]
    if env_filename:
        cmd += [ '--env-file', env_filename]

    cmd += [ 'up', '-d' ]
    subprocess.run(cmd, check=True)

    # All done, go back to original working dir.
    os.chdir(orig_dir)


def _copy(src, dest):
    if (platform.system() == 'Windows'):
        _windows_copy(src, dest)
    else:
        _unix_copy(src, dest)


def _delete(path):
    if (platform.system() == 'Windows'):
        _windows_delete(path)
    else:
        _unix_delete(path)


def _windows_copy(src, dest):
    copy_cmd = [
        'xcopy', '/e', '/i',
        src,
        dest
    ]
    subprocess.run(copy_cmd, check=True, shell=True)


def _unix_copy(src, dest):
    copy_cmd = [
        'cp', '-r',
        src,
        dest
    ]
    subprocess.run(copy_cmd, check=True)


def _windows_delete(path):
    if os.path.exists(path):
        rm_cmd = [
            'rd', '/s', '/q', path
        ]
        subprocess.run(rm_cmd, check=True, shell=True)


def _unix_delete(path):
    rm_cmd = [
        'rm', '-rf', path
    ]
    subprocess.run(rm_cmd, check=True)

# ------------------------------------------------------------
# This is the magic that runs the main function when this is invoked
# as a script.

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
