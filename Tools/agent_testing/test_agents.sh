#### USAGE: 
# ./test_agents.sh <config_file>.json


# helper func: uploads trial to elastic, runs a replay with it, and exports the trial as 'ci_replay.metadata'
run_replay() {
	echo -e "Importing source metadata file ${source_file}\n"
	output=`curl -F "file=@${source_file}" "localhost:8080/replays/import?index=logstash&createIndex=True"`
	echo ${output} | jq -rc '.message'

	read -r firstline<${source_file}
	# source_id="$(echo ${firstline} | jq -r -c '.msg.trial_id' | sed 's/[[:space:]]//g')"
	source_id="$(echo ${firstline} | jq -r -c '.msg.replay_id' | sed 's/[[:space:]]//g')"

	#url="localhost:8080/trials/run/replay/blocking/${source_id}?index=logstash"
	url="localhost:8080/replays/run/replay/blocking/${source_id}?index=logstash"
	ignore_list="{\"ignore_message_list\": [],\"ignore_source_list\": [],\"ignore_topic_list\": []}"

	echo -e "\nRunning replay from source with ID ${source_id}"

	output=`curl -X POST "$url" -H "Content-Type:application/json" -d "$ignore_list"`
	replay_id="$(echo "${output}" | jq -r -c '.data.replay_id' | sed 's/[[:space:]]//g')"
	echo ${output} | jq -rc '.message'

	echo -e "\nReplay finished: \n$output\n"

	echo -e "\nExporting replay ${replay_id}"
	curl -X GET "localhost:8080/replays/export/${replay_id}?index=logstash" > ci_replay.metadata

	read -r replay_header<ci_replay.metadata
}

# run each comparator in config file
run_comparators() {
	for cmp in $(echo "$config_entry" | jq -r '.comparators | .[]'); do
		
		# create log directory for agent if it does not exist (only first for now)
		agent_name=$(echo "$config_entry" | jq -r '.agent_names | .[0]')
		if [ ! -d "data/$agent_name" ]; then
			mkdir "data/$agent_name"
		fi
		if [ ! -d "data/$agent_name/logs" ]; then
			mkdir "data/$agent_name/logs"
		fi
		
		# run comparator and log output (.sh or .py)
		extension=${cmp##*.}
		messages=$(echo "$config_entry" | jq -r '.test_messages | .[]')
		echo -e "Running $cmp...\n"
		if [ "$extension" == "sh" ]; then 
			sh comparators/"$cmp" ci_replay.metadata "$source_file" "$messages" > "data/$agent_name/logs/$agent_name-$(date +"%m-%d-%H-%M")-${cmp%%.*}.txt"
		elif [ "$extension" == "py" ]; then
			python3 comparators/"$cmp" ci_replay.metadata "$source_file" "$messages" > "data/$agent_name/logs/$agent_name-$(date +"%m-%d-%H-%M")-${cmp%%.*}.txt"
			RC=$?
			if [ $RC -eq "0" ]; then
				echo "Test passed"
			else
				echo "Test failed"
			fi

		else
			echo -e "\nFiletype $extension not supported"
		fi
	done
}


# helper func: queries elastic for validation error messages triggered by agent under test in latest replay
log_validation_error_msgs() {
	
	# pull timestamp out of replay file
	header=$(head -n 1 ci_replay.metadata)
	echo $header > timestamps.txt
	timestamp=$(jq [.[].timestamp][0] timestamps.txt | tr -d '"')

	# log validation errors
	curl -XGET "localhost:9200/logstash*/_search?size=10000" -H "Content-Type:application/json" -d \
	'
    {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "topic.keyword": "status\/mqttvalidationservice\/messages"
                        }
                    },
                    {
                        "match": {
                            "msg.source": "'"$agent_name"'"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "'"$timestamp"'"
                            }
                        }
                    }
                ]
            }
        }
    }' > "data/$agent_name/logs/$agent_name-$(date +"%m-%d-%H-%M")-validation-errors.txt"
}






########################## MAIN ##########################

outfile="test_output.txt"

# write header for test output file
cd AgentPredicateTests
python3 write_table_header.py "$outfile"
cd -

# run replay and tests for each config entry
jq -c '.[]' "$1" | while read config_entry; do
	
	# bring up agents
	for dir in $(echo "$config_entry" | jq -r '.agent_directories | .[]');	do
		echo -e "Setting up agents...\n"
		cd "../../$dir"
		if test -f "settings.env"; then
			docker-compose --env-file settings.env up -d
		else
			docker-compose up -d
		fi
		cd -
	done

	# pull trial filename and test messages out of config file 
	source_file="$(echo "$config_entry" | jq -r '.source_file')"
	ignore_messages=$(echo "$config_entry" | jq -r '.ignore_messages')
	
	# run replay with trial and export as ci_replay.metadata
	run_replay
	
	# run tests for agents named in config
	cd AgentPredicateTests
	python3 run_specified_agent_tests.py "../$source_file" "$outfile" "$(echo "$config_entry" | jq -r '.agent_names | .[]')"
	cd -

	
	# cleanup
	for dir in $(echo "$config_entry" | jq -r '.agent_directories | .[]');	do
		echo -e "Taking down agents...\n"
		cd "../../$dir"
		docker-compose down
		cd -
	done
done
