#!/bin/bash

# Get the top-level ASIST testbed repo directory. The pushd/popd commands use
# this directory, so that this script can be safely executed from any
# directory.
export root_dir="$( cd "$(dirname "${BASH_SOURCE[0]}" )/../" >/dev/null 2>&1 && pwd)"
cd $root_dir/Local

helpFunction()
{
    echo ""
    echo "Usage: $0 [-c]"
    echo -e "\t-c Remove all remaining containers"
    exit 1
}

remove_all_containers="true"

while getopts "c" opt
do
        case "$opt" in
                c ) remove_all_containers="false";;
        esac
done

echo "Bring down ELK"
pushd ../ELK-Container
    docker-compose down --remove-orphans
popd

echo "Bring down metadata server"
pushd ../metadata/metadata-docker
    docker-compose down --remove-orphans
popd

echo "Bring down export/import dashboard"
pushd ../metadata/metadata-web
    docker-compose down --remove-orphans
popd

echo "Bring down AC_Aptima_TA3_measures"
pushd ../Agents/AC_Aptima_TA3_measures
echo Bring down Measures
docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down Gallup Agent GELP"
pushd ../Agents/gallup_agent_gelp
echo Bring down Gallup Agent GELP
docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down Gallup Agent GOLD"
pushd ../Agents/gallup_agent_gold
echo Bring down Gallup Agent GOLD
docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down AC_IHMC_TA2_Location-Monitor Agent"
pushd ../Agents/AC_IHMC_TA2_Location-Monitor
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down AC_IHMC_TA2_Player-Proximity Agent"
pushd ../Agents/AC_IHMC_TA2_Player-Proximity
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down AC_IHMC_TA2_Dyad-Reporting Agent"
pushd ../Agents/AC_IHMC_TA2_Dyad-Reporting
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down AC_IHMC_TA2_Joint-Activity-Interdependence Agent"
pushd ../Agents/AC_IHMC_TA2_Joint-Activity-Interdependence
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down AC_CMUFMS_TA2_Cognitive Agent"
pushd ../Agents/AC_CMUFMS_TA2_Cognitive
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down AC_CMU_TA1_PyGLFoV Agent"
pushd ../Agents/AC_CMU_TA1_PyGLFoVAgent
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down the ASR Agent"
pushd ../Agents/AC_UAZ_TA1_ASR_Agent
	asr_backend="GOOGLE"
	if [ "$asr_backend" = "GOOGLE" ]; then
		docker-compose -f google.yml down --volumes  --remove-orphans
	else	
		docker-compose -f vosk.yml down --volumes  --remove-orphans
	fi
popd

echo "Bring down the Speech Analyzer"
pushd ../Agents/AC_UAZ_TA1_SpeechAnalyzer
	docker-compose down --remove-orphans
popd

echo "Bring down the UAZ Dialog Agent"
pushd ../Agents/uaz_dialog_agent
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        docker-compose --env-file .env down --remove-orphans
    else
        docker-compose down --remove-orphans
    fi
popd

echo "Bring down the CMU TA2 Team Effectiveness Diagnostic AC"
pushd ../Agents/AC_CMU_TA2_TED
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down the CMU TA2 BEARD AC"
pushd ../Agents/AC_CMU_TA2_BEARD
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down the CMU TA1 ATLAS agent"
pushd ../Agents/ASI_CMU_TA1_ATLAS
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down the UAZ TMM Agent"
pushd ../Agents/ASI_UAZ_TA1_ToMCAT
        docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down the SIFT Asistant Agent"
pushd ../Agents/SIFT_Asistant_Agent
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down the atomic agent"
pushd ../Agents/atomic_agent
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down Rutgers Utility AC"
pushd ../Agents/RutgersUtilityAC
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down Minecraft"
pushd ../Local
    docker-compose -f docker-compose.asistmod.yml down --remove-orphans
    echo Deleting Minecraft data volume
    # FIXME prompts user for removing write protected file.
    rm -r ./MinecraftServer/data
popd

echo "Bring down the Doll/MIT Rita Agent"
pushd ../Agents/Rita_Agent
    docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down the CRA PSI-Coach Agent"
pushd ../Agents/ASI_CRA_TA1_psicoach
	docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down Cornell team trust AC"
pushd ../Agents/ac_cornell_ta2_teamtrust
    docker-compose down --remove-orphans
popd

# echo "Bringing down the Cornell ASI facework AC"
# pushd ../Agents/ac_cornell_ta2_asi-facework
#     docker-compose down --remove-orphans
# popd

echo "Bring down UCF Player Profiler  AC"
pushd ../Agents/AC_UCF_TA2_PlayerProfiler
    docker-compose --env-file settings.env -f docker-compose.launcher.yml down --remove-orphans
popd

echo "Bring down MQTT"
pushd ../mqtt
    docker-compose down --remove-orphans
popd

echo "Stop the the rest of the containers"

if [ $remove_all_containers = "true" ]
then
	if [[ ! -z $(docker container ls -q ) ]]; then
		docker container stop $(docker container ls -q )
	fi
else
	echo "Additional containers were not removed."
fi

docker ps
exit 0
