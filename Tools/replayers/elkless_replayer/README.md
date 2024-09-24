ELKless Replayer
================


ELKless Replayer is a simple program to replay messages from a file
containing messages collected during a TA3 experimental trial and dumped from
an Elasticsearch database.

For each line in the input file, it extracts the JSON-serialized message and
the topic it was published to, sorts all the messages by their timestamps, and
republishes the messages to the same topic that they were originally published
on.

Requirements: Python 3, a running MQTT message broker (like Mosquitto).

The script also depends on the packages listed in `requirements.txt`. You can
install them using `pip install -r requirements.txt`.

To see the command line arguments and invocation pattern, run
    ./elkless_replayer -h

There are multiple replayer tools in `Tools/replayers` - you might choose this
one if:

- you want to avoid setting up the ELK stack and know how to start up an MQTT
  message broker like `mosquitto` yourself.
- you want to enforce delays between publishing of the messages that correspond
  to the difference between the timestamps in the `header.timestamp` field of
  the messages (you can do this by adding the `-s` flag to the command-line
  invocation). The ELKless replayer tool uses a simple `time.sleep(...)` call
  in the loop that publishes the messages to the bus, compared to the
  Playback.py tool developed by CRA, which uses the Python `sched` module to
  schedule message publishing.  Using the `sched` can result in a message being
  potentially published immediately after the previous one if the previous
  message took longer to publish than the calculated timestamp between the
  messages. This can result in not enough time for downstream components to
  process the first message before the second message is published. The
  approach implemented in the ELKless replayer avoids this issue, prioritizing
  giving downstream components enough time to process upstream messages.
  However, this approach may result in a slight increase in the overall time it
  takes to replay a complete set of messages from a trial.
  
Please contact Adarsh (adarsh@arizona.edu) for support for this tool.
