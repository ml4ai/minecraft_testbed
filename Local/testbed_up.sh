#!/bin/bash

set -e
set -u
set -o nounset

# Script to automatically launch the testbed on Linux and macOS systems.
# Usage: ./testbed_up.sh

# Get the top-level ASIST testbed repo directory. The pushd/popd commands use
# this directory, so that this script can be safely executed from any
# directory.
export root_dir="$( cd "$(dirname "${BASH_SOURCE[0]}" )/../" >/dev/null 2>&1 && pwd)"

helpFunction()
{
    echo ""
    echo "Usage: $0 [-h] [-l] [-p] [-j] [-k] [-f] [-g] [-a] [-w] [-d] [-t] [-r] [-e] [-u] [-c] [-x]"
    echo "    [-s] [-m] [-o] [-b] [-y] [-n]"
    echo -e "\t-h display help text"
    echo -e "\t-l Do not start up the AC_IHMC_TA2_Location-Monitor"
    echo -e "\t-p Do not start up the IHMC Proximity/Dyad AC agents"
    echo -e "\t-j Do not start up the IHMC Joint Activity Interdependence AC agents"
    echo -e "\t-k Do not start up the CMUFMS Cognitive Load AC agents"
    echo -e "\t-f Do not start up the the CMU FoV agent"
    echo -e "\t-g Do not start up the Gallup GELP agent"
    echo -e "\t-n Do not start up the Gallup GOLD agent"
    echo -e "\t-a Do not start up the UAZ ASR agent"
    echo -e "\t-w Do not start up the UAZ speechAnalyzer agent"
    echo -e "\t-d Do not start up the UAZ Dialog agent"
    echo -e "\t-t Do not start up the UAZ TMM agent"
    echo -e "\t-r Do not start up the Doll/MIT Rita agent"
    echo -e "\t-e Do not start up the CMU TA2 Team Effectiveness Diagnostic agent"
    echo -e "\t-v Do not start up the CMU TA2 BEARD agent"
    echo -e "\t-u Do not start up the the Rutgers Utility agent"
    echo -e "\t-c Do not start up the CMU-TA1 ATLAS intervention agent"
    echo -e "\t-s Do not start up the SIFT agent"
    echo -e "\t-x Do not start up the atomic agent"
    echo -e "\t-m Do not start up the Aptima TA3 Measures agent"
    echo -e "\t-o Do not start up the CRA PSI-Coach agent"
    echo -e "\t-b Do not start up the Cornell Team Trust agent"
    echo -e "By default all agents are started up."
    exit 1
}

dont_run_lm="false"
dont_run_prox_ac="false"
dont_run_joint_activity_interdependence_ac="false"
dont_run_cmufms_cognitive_load_ac="false"
dont_run_fov="false"
dont_run_asr="false"
dont_run_speech_analyzer="false"
dont_run_dialog="false"
dont_run_tmm="false"
dont_run_gallup_agent_gelp="false"
dont_run_gallup_agent_gold="false"
dont_run_rita="false"
dont_run_cmuta2_ted="false"
dont_run_cmuta2_beard="false"
dont_run_utility="false"
dont_run_cmu_atlas="false"
dont_run_sift_agent="false"
dont_run_atomic_agent="false"
dont_run_measures="false"
dont_run_psicoach="false"
dont_run_cornell_team_trust_agent="false"

while getopts "abcdefghjklmnoprstuvwx" opt
do
        case "$opt" in
                l ) dont_run_lm="true";;
                p ) dont_run_prox_ac="true";;
                j ) dont_run_joint_activity_interdependence_ac="true";;
                k ) dont_run_cmufms_cognitive_load_ac="true";;
                f ) dont_run_fov="true";;
                g ) dont_run_gallup_agent_gelp="true";;
                n ) dont_run_gallup_agent_gold="true";;
                a ) dont_run_asr="true";;
                w ) dont_run_speech_analyzer="true";;
                d ) dont_run_dialog="true";;
                t ) dont_run_tmm="true";;
                r ) dont_run_rita="true";;
                e ) dont_run_cmuta2_ted="true";;
                v ) dont_run_cmuta2_beard="true";;
                u ) dont_run_utility="true";;
                c ) dont_run_cmu_atlas="true";;
                s ) dont_run_sift_agent="true";;
                x ) dont_run_atomic_agent="true";;
                m ) dont_run_measures="true";;
                o ) dont_run_psicoach="true";;
                b ) dont_run_cornell_team_trust_agent="true";;
                h ) helpFunction ;;
        esac
done


echo "the value of dont_run_lm after is: $dont_run_lm"
echo "the value of dont_run_prox_ac after is: $dont_run_prox_ac"
echo "the value of dont_run_joint_activity_interdependence_ac after is: $dont_run_joint_activity_interdependence_ac"
echo "the value of dont_run_cmufms_cognitive_load_ac after is: $dont_run_cmufms_cognitive_load_ac"
echo "the value of dont_run_fov after is: $dont_run_fov"
echo "the value of dont_run_asr after is: $dont_run_asr"
echo "the value of dont_run_asr after is: $dont_run_speech_analyzer"
echo "the value of dont_run_dialog after is: $dont_run_dialog"
echo "the value of dont_run_tmm after is: $dont_run_tmm"
echo "the value of dont_run_gallup_agent_gelp after is: $dont_run_gallup_agent_gelp"
echo "the value of dont_run_gallup_agent_gold after is: $dont_run_gallup_agent_gold"
echo "the value of dont_run_rita after is: $dont_run_rita"
echo "the value of dont_run_cmuta2_ted after is: $dont_run_cmuta2_ted"
echo "the value of dont_run_cmuta2_beard after is: $dont_run_cmuta2_beard"
echo "the value of dont_run_utility after is: $dont_run_utility"
echo "the value of dont_run_cmu_atlas after is: $dont_run_cmu_atlas"
echo "the value of dont_run_sift_agent after is: $dont_run_sift_agent"
echo "the value of dont_run_atomic_agent after is: $dont_run_atomic_agent"
echo "the value of dont_run_measures after is: $dont_run_measures"
echo "the value of dont_run_psicoach after is: $dont_run_psicoach"
echo "the value of dont_run_cornell_team_trust_agent after is: $dont_run_cornell_team_trust_agent"

# Determine version number
echo "Determining version number"
pushd ..
    git describe --tags >version.txt
popd

REV_TAG=$(cat ../version.txt)

echo "Testbed version:$REV_TAG"

echo "Create the asist network"
if docker network ls | grep -q "asist_net" 
then
    echo "asist_net found ... no need to create it."
else
    echo "asist_net not found ... let's create it."
    docker network create asist_net
fi

set -x
docker network ls
set +x

echo "Bringing up the MQTT broker"
pushd "$root_dir"/mqtt
    docker-compose up -d
    echo "Finished launching the Mosquitto container, waiting for 5 seconds to ensure "\
         "everything works properly..."
    sleep 5
popd

echo "Bringing up the ELK stack"
pushd "$root_dir"/ELK-Container
    docker-compose up -d --build
    echo "Finished launching the ELK stack, waiting for 5 seconds to ensure "\
         "everything works properly..."
popd

echo "Bringing up the metadata server"
pushd "$root_dir"/metadata/metadata-docker
    echo "setting version number for metadata-app"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS has BSD sed, which requires an extra argument with -i
        sed -i '' '/TESTBED_VERSION=/c\'$'\n'"TESTBED_VERSION=${REV_TAG}" metadata-app.env
    else
        sed -i "/TESTBED_VERSION=/c\TESTBED_VERSION=${REV_TAG}" metadata-app.env
    fi
    docker-compose up --build -d
popd

if [ $dont_run_measures = "false" ]; then
    echo "Bringing up AC_Aptima_TA3_measures"
    pushd "$root_dir"/Agents/AC_Aptima_TA3_measures
        docker-compose --env-file settings.env up -d
    popd
fi

if [ $dont_run_lm = "false" ]; then
    echo "Bringing up the AC_IHMC_TA2_Location-Monitor Agent"
    pushd "$root_dir"/Agents/AC_IHMC_TA2_Location-Monitor;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bring up AC_IHMC_TA2_Location-Monitor Agent"
fi

if [ $dont_run_prox_ac = "false" ]
then
    echo "Bringing up the AC_IHMC_TA2 Dyad-Reporting and Player-Proximity Agents"
    pushd "$root_dir"/Agents/AC_IHMC_TA2_Player-Proximity;docker-compose --env-file settings.env up -d
    popd
    pushd "$root_dir"/Agents/AC_IHMC_TA2_Dyad-Reporting;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bring up AC_IHMC_TA2 Dyad-Reporting and Player-Proximity Agents"
fi

if [ $dont_run_joint_activity_interdependence_ac = "false" ]
then
    echo "Bringing up the AC_IHMC_TA2_Joint-Activity-Interdependence AC Agent"
    pushd "$root_dir"/Agents/AC_IHMC_TA2_Joint-Activity-Interdependence;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bring up AC_IHMC_TA2_Joint-Activity-Interdependence AC Agents"
fi

if [ $dont_run_cmufms_cognitive_load_ac = "false" ]
then
    echo "Bringing up the AC_CMUFMS_TA2_Cognitive AC Agent"
    pushd "$root_dir"/Agents/AC_CMUFMS_TA2_Cognitive;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bring up AC_CMUFMS_TA2_Cognitive AC Agents"
fi

if [ $dont_run_fov = "false" ]
then
    echo "Bringing up the AC_CMU_TA1_PyGLFoV Agent"
    pushd "$root_dir"/Agents/AC_CMU_TA1_PyGLFoVAgent;docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up Field of view agent"
fi

if [ $dont_run_asr = "false" ]
then
    echo "Bringing up the ASR Agent"
    pushd "$root_dir"/Agents/AC_UAZ_TA1_ASR_Agent
    	asr_backend="GOOGLE"
	if [ "$asr_backend" = "GOOGLE" ]; then
		# Handle missing Google application credential file
		if [ ! -f google_application_credentials.json ]; then
		    echo "[WARNING] The Google application credentials file" \
		     "(testbed/Agents/AC_UAZ_TA1_ASR_Agent/google_application_credentials.json)" \
		     "was not found. The ASR Agent will not work." \
		     "docker-compose is going to create a directory named" \
		    "$root_dir/Agents/AC_UAZ_TA1_ASR_Agent/google_application_credentials.json" \
		    "since the file is mounted as a volume in the " \
		    "$root_dir/Agents/AC_UAZ_TA1_ASR_Agent/docker-compose.yml file." \
		    "We are not exiting this script with an error because we would like" \
		    "to exercise it in the continuous integration workflow to see if the"\
		    "container comes up even without the"\
		    "google_application_credentials.json file. However, in order for the"\
		    "container to actually work, you will need to replace the"\
		    "google_application_credentials.json directory with the actual"\
		    "credentials file."\
		    "However, in order for the container to actually work, you " \
            	    "will need to replace the google_application_credentials.json" \
                    "directory with the actual credentials file. "
		    if [ ! -z "${CI:-}" ]; then
                    	echo "We are not exiting this script with an error because we would like" \
                	"to exercise it in the continuous integration workflow to see if the"\
                	"container comes up even without the"\
                	"google_application_credentials.json file."
            	    else
                	echo "[ERROR] We are exiting this script due to the missing " \
                	"google_application_credentials.json file because it " \
                	"is not running in a Gitlab CI pipeline."
                	
			exit 1
            	    fi
		fi
		docker-compose -f google.yml up -d
	else 
		docker-compose -f vosk.yml up -d
	fi

    popd
else
    echo "Skipping bringing up ASR agent"
fi


if [ $dont_run_speech_analyzer = "false" ]; then
    echo "Bringing up the UAZ Speech Analyzer Agent"
    pushd "$root_dir"/Agents/AC_UAZ_TA1_SpeechAnalyzer
        docker-compose up -d
    popd
else
    echo "Skipping bringing up the UAZ Speech Analyzer Agent"
fi

if [ $dont_run_dialog = "false" ]; then
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
        docker-compose up -d
    popd
else
    echo "Skipping bringing up the UAZ Dialog agent"
fi

if [ $dont_run_psicoach = "false" ]; then
    echo "Bringing up the CRA PSI-Coach Agent"
    pushd "$root_dir"/Agents/ASI_CRA_TA1_psicoach
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up the CRA PSI-Coach agent"
fi

if [ $dont_run_tmm = "false" ]; then
    echo "Bringing up the UAZ TMM Agent"
    pushd "$root_dir"/Agents/ASI_UAZ_TA1_ToMCAT
            docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up the UAZ TMM agent"
fi

if [ $dont_run_gallup_agent_gelp = "false" ]; then
    echo "Bringing up Gallup Agent GELP"
    pushd "$root_dir"/Agents/gallup_agent_gelp
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up Gallup Agent GELP"
fi

if [ $dont_run_gallup_agent_gold = "false" ]; then
    echo "Bringing up Gallup Agent GOLD"
    pushd "$root_dir"/Agents/gallup_agent_gold
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up Gallup Agent GOLD"
fi

if [ $dont_run_sift_agent = "false" ]
then
    echo "Bringing up the SIFT Asistant Agent"
    pushd "$root_dir"/Agents/SIFT_Asistant_Agent
      docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up SIFT Asistant Agent"
fi

if [ $dont_run_atomic_agent = "false" ]
then
    echo "Bringing up the atomic agent"
    pushd "$root_dir"/Agents/atomic_agent
      docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up atomic agent"
fi

if [ $dont_run_cmuta2_ted = "false" ]; then
    echo "Bringing up CMU TA2 Team Effectiveness Diagnostic AC"
    pushd "$root_dir"/Agents/AC_CMU_TA2_TED
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up CMU TA2 Team Effectiveness Diagnostic AC"
fi

if [ $dont_run_cmuta2_beard = "false" ]; then
    echo "Bringing up CMU TA2 BEARD AC"
    pushd "$root_dir"/Agents/AC_CMU_TA2_BEARD
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up CMU TA2 BEARD AC"
fi

if [ $dont_run_utility = "false" ]
then
    echo "Bringing up the Rutgers Utility AC"
    pushd "$root_dir"/Agents/RutgersUtilityAC
      docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up Rutgers Utility Agent"
fi

if [ $dont_run_cornell_team_trust_agent = "false" ]
then
    echo "Bringing up the Cornell team trust AC"
    pushd "$root_dir"/Agents/ac_cornell_ta2_teamtrust
      docker-compose up -d
    popd
else
    echo "Skipping bringing up Cornell team trust AC"
fi

echo "Bring up Import/Export dashboard"
pushd ../metadata/metadata-web
    echo "setting version number for Import-Export"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS has BSD sed, which requires an extra argument with -i
        sed -i '' '/TESTBED_VERSION=/c\'$'\n'"TESTBED_VERSION=${REV_TAG}" metadata-web.env
    else
        sed -i "/TESTBED_VERSION=/c\TESTBED_VERSION=${REV_TAG}" metadata-web.env
    fi
    docker-compose up --build -d
popd



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

echo "Bringing up Minecraft"
pushd "$root_dir"/Local

    echo Copying over Minecraft data volume
    mkdir -p ./MinecraftServer
    cp -r ./data ./MinecraftServer/data

    set_permissions CLEAN_MAPS 777
    set_permissions MinecraftServer 777

    echo "setting version number for ASIST Control Center"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS has BSD sed, which requires an extra argument with -i
        sed -i '' "s/\"system_version\": .*/\"system_version\": \"${REV_TAG}\",/" MalmoControl/appsettings.Production.json
    else
        sed -i "s/\"system_version\": .*/\"system_version\": \"${REV_TAG}\",/" MalmoControl/appsettings.Production.json
    fi

    if ! sudo docker-compose -f docker-compose.asistmod.yml up -d; then
        echo "Unable to launch the MCRVM stack. Exiting now"
        exit 1
    fi
popd

if [ $dont_run_rita = "false" ]; then
    echo "Bringing up the Doll/MIT Rita Agent"
    pushd "$root_dir"/Agents/Rita_Agent
        echo "$PWD: Starting Rita Agent"
        dte=$(date "+%B-%Y-%d--%H")
        log_dir="logs-${dte}"
        export SERVICE_LOGS_DIR="$PWD/$log_dir/"
        echo "${SERVICE_LOGS_DIR} Log dirs for this instantiation of Rita"
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up the Doll/MIT Rita agent"
fi

if [ $dont_run_cmu_atlas = "false" ]
then
    echo "Bringing up the CMU-TA1 ATLAS Agent"
    pushd "$root_dir"/Agents/ASI_CMU_TA1_ATLAS
        docker-compose --env-file settings.env up -d
    popd
else
    echo "Skipping bringing up CMU-TA1 ATLAS Agent"
fi

docker ps

echo "Testbed successfully launched."
exit 0
