This directory contains tools to gather performance information about the running testbed
1. run_cadvisor.sh
This is a script file that runs the cAdvisor Docker image developed by Google.
cAdvisor gathers a large number of metrics and hosts a performance monitoring website.
The website can be found at http://<testbed_host>:8086/
The port number can be changed in the script file if you installation has a conflict with port 8086
cAdvisor mainly works on Linux (even though it is a docker image) because of how it gathers performance data. 
You might get a few metrics out of it on Windows, but Windows is not supported.

2. perf.py
This is a python script that uses the Docker API to pull several performance metrics from the docker server.
The script gathers performance metrics every 10 seconds 100 times, then exists.  These parameters can be changed in the code
The performance metrics are written to a CVS file for analysis.
