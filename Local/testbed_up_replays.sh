#!/bin/bash

set -e
set -u
set -o nounset

# Script to automatically launch the testbed on Linux and macOS systems.
# Usage: ./testbed_these_up.sh

# Get the top-level ASIST testbed repo directory. The pushd/popd commands use
# this directory, so that this script can be safely executed from any
# directory.
export root_dir="$( cd "$(dirname "${BASH_SOURCE[0]}" )/../" >/dev/null 2>&1 && pwd)"

helpFunction()
{
    echo ""
    echo "Usage: $0 [-h] [-b] [i] [-l] [-j] [-k] [-p] [-f] [-g] [-a] [-w] [-d] [-t] [-r] [-e] [-u] [-c]"
    echo "    [-s] [-m] [-o] [-q] [-y] [-n]"
    echo -e "\t-h display help text"
	echo -e "\t-b Do not start up core testbed components [Default:startup]"
	echo -e "\t-i Start up all ACs [Default:do not start]"
    echo -e "\t-l Start up the IHMC Location Monitor agent"
    echo -e "\t-p Start up the IHMC Proximity/Dyad AC agents"
    echo -e "\t-j Start up the IHMC Joint Activity Interdependence AC agent"
    echo -e "\t-k Start up the CMUFMS Cognitive Load AC agent"
    echo -e "\t-f Start up the the CMU FoV agent"
    echo -e "\t-g Start up the Gallup GELP agent"
    echo -e "\t-n Start up the Gallup GOLD agent"
    echo -e "\t-a Start up the UAZ ASR agent"
    echo -e "\t-w Start up the UAZ SpeechAnalyzer agent"
    echo -e "\t-d Start up the UAZ Dialog agent"
    echo -e "\t-t Start up the UAZ TMM agent"
    echo -e "\t-r Start up the Doll/MIT Rita agent"
    echo -e "\t-e Start up the CMU TA2 Team Effectiveness Diagnostic agent"
    echo -e "\t-v Start up the CMU TA2 BEARD agent"
    echo -e "\t-u Start up the the Rutgers Utility agent"
    echo -e "\t-c Start up the CMU-TA1 ATLAS agent"
    echo -e "\t-s Start up the SIFT agent"
    echo -e "\t-x Start up the atomic agent"
    echo -e "\t-m Start up the Aptima TA3 Measures agent"
    echo -e "\t-o Start up the CRA PSI-Coach agent"
    echo -e "\t-q Start up the UCF Player Profiler agent"
    echo -e "By default only core components are started and select key agents."
    exit 1
}
do_run_core="true"
do_run_lm="false"
do_run_prox_ac="false"
do_run_jai_ac="false"
do_run_cmufms_cl_ac="false"
do_run_fov="false"
do_run_asr="false"
do_run_speech_analyzer="false"
do_run_dialog="false"
do_run_tmm="false"
do_run_gallup_agent_gelp="false"
do_run_gallup_agent_gold="false"
do_run_rita="false"
do_run_cmuta2_ted="false"
do_run_cmuta2_beard="false"
do_run_utility="false"
do_run_cmu_atlas="false"
do_run_sift_agent="false"
do_run_atomic_agent="false"
do_run_measures="false"
do_run_psicoach="false"
do_run_all_acs="false"
do_run_cornell_team_trust="false"
do_run_ucf_player_profiler="false"

while getopts "lpjkfgnawdtrevucsmohbiq" opt
do
        case "$opt" in
                l ) do_run_lm="true";;
                p ) do_run_prox_ac="true";;
                j ) do_run_jai_ac="true";;
                k ) do_run_cmufms_cl_ac="true";;
                f ) do_run_fov="true";;
                g ) do_run_gallup_agent_gelp="true";;
                n ) do_run_gallup_agent_gold="true";;
                a ) do_run_asr="true";;
                w ) do_run_speech_analyzer="true";;
                d ) do_run_dialog="true";;
                t ) do_run_tmm="true";;
                r ) do_run_rita="true";;
                e ) do_run_cmuta2_ted="true";;
                v ) do_run_cmuta2_beard="true";;
                u ) do_run_utility="true";;
                c ) do_run_cmu_atlas="true";;
                s ) do_run_sift_agent="true";;
                x ) do_run_atomic_agent="true";;
                m ) do_run_measures="true";;
                o ) do_run_psicoach="true";;
                q ) do_run_ucf_player_profiler="true";;
                b ) do_run_core="false";;
                i ) do_run_all_acs="true";;
                h ) helpFunction ;;
        esac
done

echo "the value of do_run_core after is: $do_run_core"
echo "the value of do_run_all_acs after is: $do_run_all_acs"
echo "the value of do_run_lm after is: $do_run_lm"
echo "the value of do_run_prox_ac after is: $do_run_prox_ac"
echo "the value of do_run_jai_ac after is: $do_run_jai_ac"
echo "the value of do_run_cmufms_cl_ac is: $do_run_cmufms_cl_ac"
echo "the value of do_run_fov after is: $do_run_fov"
echo "the value of do_run_asr after is: $do_run_asr"
echo "the value of do_run_speech_analyzer after is: $do_run_speech_analyzer"
echo "the value of do_run_dialog after is: $do_run_dialog"
echo "the value of do_run_tmm after is: $do_run_tmm"
echo "the value of do_run_gallup_agent_gelp after is: $do_run_gallup_agent_gelp"
echo "the value of do_run_gallup_agent_gold after is: $do_run_gallup_agent_gold"
echo "the value of do_run_rita after is: $do_run_rita"
echo "the value of do_run_cmuta2_ted after is: $do_run_cmuta2_ted"
echo "the value of do_run_cmuta2_beard after is: $do_run_cmuta2_beard"
echo "the value of do_run_utility after is: $do_run_utility"
echo "the value of do_run_cmu_atlas after is: $do_run_cmu_atlas"
echo "the value of do_run_sift_agent after is: $do_run_sift_agent"
echo "the value of do_run_atomic_agent after is: $do_run_atomic_agent"
echo "the value of do_run_measures after is: $do_run_measures"
echo "the value of do_run_psicoach after is: $do_run_psicoach"
echo "the value of do_run_cornell_team_trust after is $do_run_cornell_team_trust"
echo "the value of do_run_ucf_player_profiler after is $do_run_ucf_player_profiler"

# Determine version number
echo "Updating Agent Volume Paths for docker in docker control"

./update_config_paths.sh

echo "Determining version number"
pushd ..
    echo "Getting full testbed version"
    git describe --tags > version.txt
popd

REV_TAG=$(cat ../version.txt)

echo "Testbed version:$REV_TAG"

if [[ $do_run_core = "true" ]]; then
	echo "Create the asist network"
    if docker network ls | grep -q "asist_net" 
    then
        echo "asist_net found ... no need to create it."
    else
        echo "asist_net not found ... let's create it."
        docker network create asist_net
    fi
	
fi

if [[ $do_run_core = "true" ]]; then
	echo "Bringing up the MQTT broker"
	pushd "$root_dir"/mqtt
		docker-compose --compatibility up -d
		echo "Finished launching the Mosquitto container, waiting for 5 seconds to ensure everything works properly..."
		sleep 5
	popd
fi

if [ $do_run_core = "true" ]; then
	echo "Bringing up the ELK stack"
	pushd "$root_dir"/ELK-Container
		docker-compose --compatibility up -d --build
		echo "Finished launching the ELK stack, waiting for 5 seconds to ensure "\
			 "everything works properly..."
	popd
fi

if [ $do_run_core = "true" ]; then
	echo "Bringing up the metadata server"
	pushd "$root_dir"/metadata/metadata-docker
		echo "setting version number for metadata-app"
		if [[ "$OSTYPE" == "darwin"* ]]; then
			# macOS has BSD sed, which requires an extra argument with -i
			sed -i '' '/TESTBED_VERSION=/c\'$'\n'"TESTBED_VERSION=${REV_TAG}" metadata-app.env
		else
			sed -i "/TESTBED_VERSION=/c\TESTBED_VERSION=${REV_TAG}" metadata-app.env
		fi
		docker-compose --compatibility up --build -d
	popd
fi

if [ $do_run_measures = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up the Measure Agent"
    pushd "$root_dir"/Agents/AC_Aptima_TA3_measures
        docker-compose --env-file settings.env up -d
    popd
fi

if [ $do_run_lm = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up the IHMC Location Monitor"
    pushd "$root_dir"/Agents/AC_IHMC_TA2_Location-Monitor;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bring up IHMC Location Monitor Agent"
fi

if [ $do_run_prox_ac = "true" ] || [ $do_run_all_acs = "true" ]
then
    echo "Bringing up the IHMC Proximity/Dyad AC Agents"
    pushd "$root_dir"/Agents/AC_IHMC_TA2_Player-Proximity;docker-compose --env-file settings.env up -d
    popd
    pushd "$root_dir"/Agents/AC_IHMC_TA2_Dyad-Reporting;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bring up IHMC Proximity/Dyad AC Agents"
fi

if [ $do_run_jai_ac = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up the IHMC Joint Activity Interdependence AC"
    pushd "$root_dir"/Agents/AC_IHMC_TA2_Joint-Activity-Interdependence;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bring up IHMC Joint Activity Interdependence AC"
fi

if [ $do_run_cmufms_cl_ac = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up the CMUFMS Cognitive Load AC"
    pushd "$root_dir"/Agents/AC_CMUFMS_TA2_Cognitive;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bring up CMUFMS Cognitive Load AC"
fi

if [ $do_run_fov = "true" ] || [ $do_run_all_acs = "true" ]
then
    echo "Bringing up the PyGL FoV Agent"
    pushd "$root_dir"/Agents/AC_CMU_TA1_PyGLFoVAgent;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up Field of view agent"
fi


## FROM ADARSH ON SLACK

# https://darpa-asist.slack.com/archives/CPHABHZ42/p1649962325217339?thread_ts=1649960282.749689&cid=CPHABHZ42

# For future replays, you can filter out the DialogAgent messages while keeping the ASR/SpeechAnalyzer messages 
#- the DialogAgent consumes the ASR messages rather than the raw audio chunks, so it can be launched for the replays.

# if [ $do_run_asr = "true" ] || [ $do_run_all_acs = "true" ]
# then
#     echo "Bringing up the ASR Agent"
#     pushd "$root_dir"/Agents/AC_UAZ_TA1_ASR_Agent
#     	asr_backend="GOOGLE"
#         if [ "$asr_backend" = "GOOGLE" ]; then
#                 # Handle missing Google application credential file
#                 if [ ! -f google_application_credentials.json ]; then
#                     echo "[WARNING] The Google application credentials file" \
#                      "(testbed/Agents/AC_UAZ_TA1_ASR_Agent/google_application_credentials.json)" \
#                      "was not found. The ASR Agent will not work." \
#                      "docker-compose is going to create a directory named" \
#                     "$root_dir/Agents/AC_UAZ_TA1_ASR_Agent/google_application_credentials.json" \
#                     "since the file is mounted as a volume in the " \
#                     "$root_dir/Agents/AC_UAZ_TA1_ASR_Agent/docker-compose.yml file." \
#                     "We are not exiting this script with an error because we would like" \
#                     "to exercise it in the continuous integration workflow to see if the"\
#                     "container comes up even without the"\
#                     "google_application_credentials.json file. However, in order for the"\
#                     "container to actually work, you will need to replace the"\
#                     "google_application_credentials.json directory with the actual"\
#                     "credentials file."\
#                     "However, in order for the container to actually work, you " \
#                     "will need to replace the google_application_credentials.json" \
#                     "directory with the actual credentials file. "
#                     if [ ! -z "${CI:-}" ]; then
#                         echo "We are not exiting this script with an error because we would like" \
#                         "to exercise it in the continuous integration workflow to see if the"\
#                         "container comes up even without the"\
#                         "google_application_credentials.json file."
#                     else
#                         echo "[ERROR] We are exiting this script due to the missing " \
#                         "google_application_credentials.json file because it " \
#                         "is not running in a Gitlab CI pipeline."

#                         exit 1
#                     fi
#                 fi
#                 docker-compose -f google.yml --compatibility up -d
#         else
#                 docker-compose -f vosk.yml --compatibility up -d
#         fi
#     popd
# else
#     echo "Skipping bringing up Speech Analyzer agent"
# fi

# if [ $do_run_speech_analyzer = "true" ] || [ $do_run_all_acs = "true" ]
# then
#     echo "Bringing up the Speech Analyzer Agent"
#     pushd "$root_dir"/Agents/AC_UAZ_TA1_SpeechAnalyzer
# 	docker-compose --compatibility up -d
#     popd
# else
#     echo "Skipping bringing up Speech Analyzer agent"
# fi

if [ $do_run_dialog = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up the UAZ Dialog Agent"
    pushd "$root_dir"/Agents/uaz_dialog_agent
        # We set the TAMU Dialog Act Classifier hostname (the TDAC_HOSTNAME
        # variable) to host.docker.internal for non-Linux (macOS/Windows)
        # systems, on which Docker resolves 'host.docker.internal' to the
        # internal IP address used by the host. On Linux systems the
        # TDAC_HOSTNAME variable will be set automatically by the .env file.
        if [[ ! "$OSTYPE" == "linux-gnu"* ]]; then
            export TDAC_HOSTNAME=host.docker.internal
        fi
        docker-compose --compatibility up -d
    popd
else
    echo "Skipping bringing up the UAZ Dialog agent"
fi

if [ $do_run_gallup_agent_gelp = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up Gallup Agent GELP"
    pushd "$root_dir"/Agents/gallup_agent_gelp
        docker-compose --env-file settings.env --compatibility up -d
    popd
else
    echo "Skipping bringing up Gallup Agent GELP"
fi

if [ $do_run_gallup_agent_gold = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up Gallup Agent GOLD"
    pushd "$root_dir"/Agents/gallup_agent_gold
        docker-compose --env-file settings.env --compatibility up -d
    popd
else
    echo "Skipping bringing up Gallup Agent GOLD"
fi

if [ $do_run_cmuta2_ted = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up CMU TA2 Team Effectiveness Diagnostic AC"
    pushd "$root_dir"/Agents/AC_CMU_TA2_TED
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up CMU TA2 Team Effectiveness Diagnostic AC"
fi

if [ $do_run_cmuta2_beard = "true" ] || [ $do_run_all_acs = "true" ]; then
    echo "Bringing up CMU TA2 BEARD AC"
    pushd "$root_dir"/Agents/AC_CMU_TA2_BEARD
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up CMU TA2 BEARD AC"
fi

if [ $do_run_utility = "true" ] || [ $do_run_all_acs = "true" ]
then
    echo "Bringing up the Rutgers Utility AC"
    pushd "$root_dir"/Agents/RutgersUtilityAC
      docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up Rutgers Utility Agent"
fi

if [ $do_run_core = "true" ]; then
	echo "Bring up Import/Export dashboard"
	pushd ../metadata/metadata-web
		echo "setting version number for Import-Export"
		if [[ "$OSTYPE" == "darwin"* ]]; then
			# macOS has BSD sed, which requires an extra argument with -i
			sed -i '' '/TESTBED_VERSION=/c\'$'\n'"TESTBED_VERSION=${REV_TAG}" metadata-web.env
		else
			sed -i "/TESTBED_VERSION=/c\TESTBED_VERSION=${REV_TAG}" metadata-web.env
		fi
		docker-compose --compatibility up --build -d
	popd
fi


# Helper function to set permissions while avoiding unnecessary entering of
# superuser password.
set_permissions() {
    local TARGET=$1
    local DESIRED_PERMISSIONS=$2
    local CURRENT_PERMISSIONS=""

    # The invocation for the 'stat' command is different on macOS and Linux
    # systems.
    if [[ "$OSTYPE" == "darwin"* ]]; then
        CURRENT_PERMISSIONS=$(stat -f "%A" CLEAN_MAPS)
    else
        CURRENT_PERMISSIONS=$(stat --format '%a' CLEAN_MAPS)
    fi

    if [[ ! $CURRENT_PERMISSIONS == "$DESIRED_PERMISSIONS" ]]; then
        echo "Changing permissions of $TARGET to $DESIRED_PERMISSIONS."
        if ! sudo chmod -R "$DESIRED_PERMISSIONS" "$TARGET"; then
            echo "Unable to perform the command 'chmod -R $DESIRED_PERMISSIONS $TARGET', "\
                "exiting now."
            exit 1
        fi
    fi
}

if [ $do_run_core = "true" ]; then
	echo "Bringing up Minecraft"
	pushd "$root_dir"/Local

		if ! sudo docker-compose -f docker-compose.replays.yml up -d; then
			echo "Unable to launch the MCRVM stack. Exiting now"
			exit 1
		fi
	popd
fi

if [ $do_run_rita = "true" ]; then
    echo "Bringing up the Doll/MIT Rita Agent"
    pushd "$root_dir"/Agents/Rita_Agent
        echo "$PWD: Starting Rita Agent"
        dte=$(date "+%B-%Y-%d")
        log_dir="logs-${dte}"
        export SERVICE_LOGS_DIR="$log_dir/"
        echo "${SERVICE_LOGS_DIR} Log dirs for this instantiation of Rita"
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up the Doll/MIT Rita agent"
fi

if [ $do_run_cmu_atlas = "true" ]
then
    echo "Bringing up the CMU-TA1 ATLAS Agent"
    pushd "$root_dir"/Agents/ASI_CMU_TA1_ATLAS
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up CMU-TA1 ATLAS Agent agent"
fi

if [ $do_run_cornell_team_trust = "true" ] || [ $do_run_all_acs = "true" ]
then
    echo "Bringing up the Cornell team trust AC"
    pushd "$root_dir"/Agents/ac_cornell_ta2_teamtrust
      docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up Cornell team trust AC"
fi

# if [ $do_run_all_acs = "true" ]
# then
#     echo "Bringing up the Cornell ASI facework AC"
#     pushd "$root_dir"/Agents/ac_cornell_ta2_asi-facework
#       docker-compose --env-file settings.env up -d
#     popd
# else
#     echo "Skipping bringin up Cornell facework AC"
# fi

if [ $do_run_ucf_player_profiler = "true" ] || [ $do_run_all_acs = "true" ]
then
    echo "Bringing up the UCF Player Profiler AC"
    pushd "$root_dir"/Agents/AC_UCF_TA2_PlayerProfiler
      docker-compose --env-file settings.env -f docker-compose.launcher.yml up -d
    popd
else
    echo "Skipping bringing up UCF Player Profiler AC"
fi

docker ps

echo "Testbed successfully launched."
exit 0
