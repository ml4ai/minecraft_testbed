import docker
import zipfile
import sys
import os

client = docker.from_env()
containers = client.containers.list(all=True)
print(containers)
do_zip = False
encoding = 'utf-8'
# get the current durectory

# check if we want to zip the logs
if len(sys.argv) > 1:
    for opt, oarg in opts:
        if opt == "-z":
            print("zipping up dozzle logs")
            do_zip = True

if do_zip:
    zf = zipfile.ZipFile("docker-logs.zip", mode="w", compression=zipfile.ZIP_DEFLATED)

for c in containers:
    print(c.attrs['Id'] + " : " + c.attrs['Name'][1:])
    container = client.containers.get(c.attrs['Id'])
    if do_zip:
        zf.writestr(c.attrs['Name'][1:] + ".log", container.logs())
    else:
        #open a file for this log
        f = open(c.attrs['Name'][1:] + ".log", "w")
        f.write(str(container.logs(), encoding))
        f.close()

if do_zip:
    zf.close()
