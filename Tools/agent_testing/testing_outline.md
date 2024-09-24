outer script: 
    for each line in config file:
        start up agent with docker_compose in agent_dir
        wait a lil bit
        if agent is up:
            import the trial
            run replay with trial
            export replay
            for each comparison method:
                switch comparison method:
                    case total_record_count: 
                        count_records(trial, replay)
                        log test results - test name, passed/failed, reason for failure
                    case specific_record_count:
                        count_specific_records(trial, replay, [messages_to_test])
                        log test results - test name, passed/failed, reason for failure
                    case fov_agent_test:
                        whatever
                        log test results - test name, passed/failed, reason for failure


directory layout: 
    ci-testing
    | test-agents.sh
    | config.json
    | comparators
    | [dir for each agent's trial file]