# set host directory to top level testbed folder
cd ..
host_directory=$(pwd)
echo "$host_directory"

# cd ../ASI_UAZ_TA1_ToMCAT
# host_directory=$(pwd)/
# sed -i "/HOST_DIRECTORY/d" ./settings.env

echo '-----UPDATING TOMCAT AGENT HOST PATH-------'

echo "HOST_DIRECTORY="$host_directory  >> ./settings.env








