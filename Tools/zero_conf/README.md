Running the Testbed with (nearly) Zero Conf
===========================================

At the end of Study 2, the Testbed required a fairly involved dance with
multiple web pages and steps to start a run. As we move to use performer agents
with the live testbed, some developers will be running the testbed and
repeatedly restarting their agent for testing. To minimize the friction and time
involved in starting a testbed run, Jeff Rye (SIFT, ry@sift.net) came up with
the approach described herein.

Note that this does not try to cover a broad base of use cases. This just gets
the testbed to a state where you can connect players and agents and start doing
things in the Minecraft world.

The default `testbed_up.sh` script brings up all kinds of containers (e.g., the
ELK stack, control interface, etc.). Here we start only the MQTT bus, the IHMC
Location agent, and the Minecraft server. This results in very quick startup, but obviously comes at the cost of logging, replay, and flexibility in general.

# Technical Details/Background

As of this writing, the minecraft server sends a request for trial info and
expects a particular response (which identifies the map, allowed players, etc.).
This was being handled by the web controller UI. Here we fake that response with
predefined values. At the same time we make an RCON connection and send commands
to remove the blocking wall without forcing a mission start.

In the end, I created a script (`lightweight_testbed.py`) that just run the
MQTT, IHMC Location Agent, and the Minecraft server. When the Minecraft server
comes up, it sends an MQTT message asking for trial information. So I have a
second script (`bootstrap_minecraft.py`) that responds with the required
information.

This trial message needs to identify the specific players that will be allowed
to connect to the Minecraft server. So the bootstrap script requires a
playername as a command line argument. I haven't figured out a way to automate
the collection of that name yet.

# Getting Started

To run the scripts in this directory, you will need a modern Python (known to
work with ^3.8) and docker/docker-compose. You will need the following Python
libraries. If you use [poetry](https://python-poetry.org/), you can simply run
`poetry install` and then run the commands below in the poetry shell.
- `mcrcon`
- `paho-mqtt`

# What to Run

Here are the specific commands to run:

1. Launch the Minecraft client and make note of the player name. Note that you
   may use your own licensed copy of Minecraft and start it how you normally do.
   If you use the [free Malmo
   client](https://github.com/Microsoft/malmo/releases), this is how to invoke
   it.

   Note that the mod in your Minecraft client needs to match the current one for
   the server. If using the free Malmo client as shown here, you can update it
   like this (before launching it.):
   ```sh
   rm ../../../Malmo-0.37.0-Mac-64bit_withBoost_Python3.7/Minecraft/run/mods/asistmod-1.0.*.jar
   cp ../../Local/data/mods/asistmod-1.0.*.jar ../../../Malmo-0.37.0-Mac-64bit_withBoost_Python3.7/Minecraft/run/mods/
   ```
   And then to actually start the client:
   ```sh
   cd ../../../Malmo-0.37.0-Mac-64bit_withBoost_Python3.7/Minecraft
   ./launchClient.sh
   ```

2. Next, start the Minecraft bootstrapper. This will connect to MQTT
   automatically and respond to the Minecraft server's query for trial info.
   When MQTT is not available (or goes away), it will continue retrying the
   connection until it succeeds. So you can just leave this running as long as
   the player name stays the same.
   ```sh
   ./bootstrap_minecraft.py PlayerXXX
   ```

3. Start ASI agents. We recommend making these work like the bootstrapper, and
   wait for an MQTT connection and reconnect automatically when needed.

4. Finally, run the testbed itself. The last command in this script runs
   `docker-compose` for the Minecraft server. It does *not* put the server in
   daemon mode. This leaves the script running and writing the Minecraft server
   output to the console. I found this to be very helpful for debugging and
   spotting problems.
   ```sh
   ./light_testbed.py
   ```

5. Watch the logs for the bootstrapper and/or testbed startup. When they show
   the client info has been handled, you can connect the Minecraft client and
   start playing. The client can connect to the Minecraft server on port 25565.

Depending on what you want to test, you may just restart the ASIST agent and
continue playing. If you need to restart the testbed: hit ctrl-c in the
`lightweight_testbed.py` and ASIST agent windows, then proceed from step 3
above.
