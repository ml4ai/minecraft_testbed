#/bin/bash

# $1==relative path of trial metadata file
# $2==JSON ignore list

echo -e "Importing trial ${1}\n"
curl -F "file=@${1}" "localhost:8080/trials/import?index=logstash&createIndex=True"
echo -e "\nImport finished\n"

read -r firstline<${1}
trial_id="$(echo ${firstline} | jq -r -c '.msg.trial_id' | sed 's/[[:space:]]//g')"
url="localhost:8080/replays/run/trial/${trial_id}?index=logstash"
ignore_list="$(echo ${2} | sed 's/"/\"/g')"
echo -e "\nRunning replay with trial ${trial_id}"
output=`curl -X POST "$url" -H "Content-Type:application/json" -d "$ignore_list"`
replay_id="$(echo "${output}" | jq -r -c '.data.replay_id' | sed 's/[[:space:]]//g')"
echo -e "\nReplay finished: \n$output\n"


echo -e "\nExporting replay ${replay_id}"
curl -X GET "localhost:8080/replays/export/${replay_id}?index=logstash" > ci_replay.metadata

read -r replay_header<ci_replay.metadata
