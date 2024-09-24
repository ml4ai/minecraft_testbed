#!/bin/bash
#get the arguments to the script. the key one is the trial id
while getopts t: flag
do
    case "${flag}" in
        t) trial_id=${OPTARG};;
    esac
done
if [ -z "$trial_id" ];
then
    trial_id="NoTrial"
else
    trial_id=${trial_id:0:8}
fi
echo "Trial id: $trial_id";

pdir=$(dirname $0)
function set_testbed_home() {
    pushd . > /dev/null
    cd ../../
    export testbed_home=$PWD
    popd > /dev/null
}
set_testbed_home

# create the working directory name with the current date and time
export dir_name="asist_logs_${trial_id}_"$(date +"%Y_%m_%d_%H_%M_%S")
echo $dir_name
# create the main directory
mkdir $dir_name
# cd into the main directory and create the dozzle log directory
cd $dir_name
mkdir dozzle_logs
cd dozzle_logs
echo "Testbed Home is $testbed_home"
# run the python script to gather all of the dozzle logs
python3 ${testbed_home}/Tools/docker-logs/docker-logs.py
#go back to the main logs directory for any other agents that want to save logs
cd ..

#template for each of the agents that wants to collect logs/data
# create a sub-directory with the name of the agent that is collecting the data
# dump what ever you want into that directory
# Go back up to the main directory for the next agent
#

# Retrieving data for SpeechAnalyzer
echo "Retrieving logs for SpeechAnalyzer and dumping features database"
mkdir SpeechAnalyzer
cd SpeechAnalyzer	
	# Dump features database
        docker exec -i AC_UAZ_TA1_SpeechAnalyzer-db /bin/bash -c "PGPASSWORD=docker pg_dump --username postgres features" > features.sql
        # Truncate table
        docker exec -it AC_UAZ_TA1_SpeechAnalyzer-db /bin/bash -c "PGPASSWORD=docker psql -U postgres -d features -c 'TRUNCATE TABLE features;'"
	# Copy logs
	cp -r $testbed_home/Agents/AC_UAZ_TA1_SpeechAnalyzer/logs .
cd ..


# Retrieving data for ASR_Agent
echo "Retrieving logs for ASR_Agent"
mkdir ASR_Agent
cd ASR_Agent	
	# Copy logs
	cp -r $testbed_home/Agents/AC_UAZ_TA1_ASR_Agent/logs .
cd ..

# Retrieving data for ToMCAT agent
echo "Retrieving logs for ToMCAT"
mkdir ToMCAT
cd ToMCAT	
	# Copy logs
	cp -r $testbed_home/Agents/ASI_UAZ_TA1_ToMCAT/logs .
cd ..

# Gather IHMC's log files
echo "Retrieving IHMC's log files"
docker exec ac_ihmc_ta2_joint-activity-interdependence sh -c "/bin/tar --create --file=ihmc-logs.tar --verbose -- *.log"
docker cp ac_ihmc_ta2_joint-activity-interdependence:/app/ihmc-logs.tar .

# Function to get rita logs
function get_rita_logs() {
  echo "Retrieving Rita Logs"
#  pushd .
  latest_log_dir=`ls -td $testbed_home/Agents/Rita_Agent/logs-* | head -1`
  dname_only=`basename $latest_log_dir`

  echo "Latest Rita Log dir $latest_log_dir"
  cp -a $latest_log_dir "rita-$dname_only"
#  popd .
}

function clean_rita_agent_logs() {
    echo "Cleaning rita agent logs"
    latest_log_dir_count=`ls -td $testbed_home/Agents/Rita_Agent/logs-* | wc -l`

    N_KEEP=7
    if [ "$latest_log_dir_count" -gt "$N_KEEP" ]; then
      let "remove = $latest_log_dir_count - $N_KEEP"

      echo "Rita Logs ${latest_log_dir_count}"
      echo "We will keep: $N_KEEP"
      echo "We will remove: $remove"
      to_remove=`ls -td $testbed_home/Agents/Rita_Agent/logs-* | tail -${remove}`
      echo "TO remove "
      echo ${to_remove}
      rm -rf ${to_remove}
    fi
}

echo "My PWD $PWD"
get_rita_logs
clean_rita_agent_logs

echo "Retrieving PSI-Coach log files"
mkdir psicoach
cd psicoach
    # Copy data artifacts
	cp $testbed_home/Agents/ASI_CRA_TA1_psicoach/logs/*.dat .
	cp $testbed_home/Agents/ASI_CRA_TA1_psicoach/logs/*.log .
cd ..

echo "Zip up the entire directory"
cd ..
echo "Current dir: $PWD"
tar -zcvf $dir_name.tar.gz $dir_name
echo "All logs captured"
