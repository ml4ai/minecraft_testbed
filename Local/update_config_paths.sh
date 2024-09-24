# set host directory to top level testbed folder
cd ..
host_directory=$(pwd)
echo "$host_directory"

cd ./Agents/atomic_agent
host_directory=$(pwd)/
sed -i "/HOST_DIRECTORY/d" ./settings.env

echo '-----UPDATING ATOMIC AGENT HOST PATH-------'

echo "HOST_DIRECTORY="$host_directory  >> ./settings.env

cd ../ASI_CMU_TA1_ATLAS
host_directory=$(pwd)/
sed -i "/HOST_DIRECTORY/d" ./settings.env

echo '-----UPDATING CMU_TA1_INTERVENTION_AGENT HOST PATH-------'

echo "HOST_DIRECTORY="$host_directory  >> ./settings.env

cd ../ASI_CRA_TA1_psicoach
host_directory=$(pwd)/
sed -i "/HOST_DIRECTORY/d" ./settings.env

echo '-----UPDATING PSICOACH AGENT HOST PATH-------'

echo "HOST_DIRECTORY="$host_directory  >> ./settings.env

cd ../Rita_Agent
host_directory=$(pwd)/
sed -i "/HOST_DIRECTORY/d" ./settings.env

echo '-----UPDATING RITA AGENT HOST PATH-------'

echo "HOST_DIRECTORY="$host_directory  >> ./settings.env

cd ../SIFT_Asistant_Agent
host_directory=$(pwd)/
sed -i "/HOST_DIRECTORY/d" ./settings.env

echo '-----UPDATING SIFT ASISTANT AGENT HOST PATH-------'

echo "HOST_DIRECTORY="$host_directory  >> ./settings.env

cd ../ASI_UAZ_TA1_ToMCAT
host_directory=$(pwd)/
sed -i "/HOST_DIRECTORY/d" ./settings.env

echo '-----UPDATING TOMCAT AGENT HOST PATH-------'

echo "HOST_DIRECTORY="$host_directory  >> ./settings.env








