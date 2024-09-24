"""Profiling Computation"""

import json
import sys

import numpy as np
import pandas as pd

NUM_SIG_FIGS = 3

# Mapping of survey variables to qualtrics IDs
# SURVEY_VARIABLES = {
#     "gaming_experience": ["QID870", "QID869"],
#     "mission_knowledge": ["SC_0dFvjllRXQzBoYR"],
#     "anger": ["QID1021_8", "QID1021_11"],
#     "anxiety": ["QID1021_7", "QID1021_15", "QID1021_18", "QID1021_20"],
#     "rmie": [
#         ("QID751", 1), ("QID753", 2), ("QID755", 3), ("QID757", 2),
#         ("QID759", 3), ("QID761", 2), ("QID763", 3), ("QID765", 1),
#         ("QID767", 4), ("QID769", 1), ("QID771", 3), ("QID773", 3),
#         ("QID775", 2), ("QID777", 4), ("QID779", 1), ("QID781", 2),
#         ("QID783", 1), ("QID785", 1), ("QID787", 4), ("QID789", 2),
#         ("QID791", 2), ("QID793", 1), ("QID795", 3), ("QID797", 1),
#         ("QID799", 4), ("QID801", 3), ("QID803", 2), ("QID805", 1),
#         ("QID807", 4), ("QID809", 2), ("QID811", 2), ("QID813", 1),
#         ("QID815", 4), ("QID817", 3), ("QID819", 2), ("QID821", 3)],
#     "sbsod": ["QID13_1", "QID13_2r", "QID13_3", "QID13_4", "QID13_5",
#               "QID13_6r", "QID13_7", "QID13_8r", "QID13_9", "QID13_10r",
#               "QID13_11r", "QID13_12r", "QID13_13r", "QID13_14", "QID13_15r"]
# }

SURVEY_VARIABLES = {
    "gaming_experience": [
        ("IntakeSurvey", "QID870"),
        ("IntakeSurvey", "QID869")],
    "mission_knowledge": [("TrainingKnowledge", "SC_0dFvjllRXQzBoYR")],
    "anger": [
        ("TrainingKnowledge", "QID1021_8"),
        ("TrainingKnowledge", "QID1021_11")],
    "anxiety": [
        ("TrainingKnowledge", "QID1021_7"),
        ("TrainingKnowledge", "QID1021_15"),
        ("TrainingKnowledge", "QID1021_18"),
        ("TrainingKnowledge", "QID1021_20")],
    "rmie": [
        ("IntakeSurvey", "QID751", 1), ("IntakeSurvey", "QID753", 2),
        ("IntakeSurvey", "QID755", 3), ("IntakeSurvey", "QID757", 2),
        ("IntakeSurvey", "QID759", 3), ("IntakeSurvey", "QID761", 2),
        ("IntakeSurvey", "QID763", 3), ("IntakeSurvey", "QID765", 1),
        ("IntakeSurvey", "QID767", 4), ("IntakeSurvey", "QID769", 1),
        ("IntakeSurvey", "QID771", 3), ("IntakeSurvey", "QID773", 3),
        ("IntakeSurvey", "QID775", 2), ("IntakeSurvey", "QID777", 4),
        ("IntakeSurvey", "QID779", 1), ("IntakeSurvey", "QID781", 2),
        ("IntakeSurvey", "QID783", 1), ("IntakeSurvey", "QID785", 1),
        ("IntakeSurvey", "QID787", 4), ("IntakeSurvey", "QID789", 2),
        ("IntakeSurvey", "QID791", 2), ("IntakeSurvey", "QID793", 1),
        ("IntakeSurvey", "QID795", 3), ("IntakeSurvey", "QID797", 1),
        ("IntakeSurvey", "QID799", 4), ("IntakeSurvey", "QID801", 3),
        ("IntakeSurvey", "QID803", 2), ("IntakeSurvey", "QID805", 1),
        ("IntakeSurvey", "QID807", 4), ("IntakeSurvey", "QID809", 2),
        ("IntakeSurvey", "QID811", 2), ("IntakeSurvey", "QID813", 1),
        ("IntakeSurvey", "QID815", 4), ("IntakeSurvey", "QID817", 3),
        ("IntakeSurvey", "QID819", 2), ("IntakeSurvey", "QID821", 3)],
    "sbsod": [
        ("IntakeSurvey", "QID13_1"), ("IntakeSurvey", "QID13_2r"),
        ("IntakeSurvey", "QID13_3"), ("IntakeSurvey", "QID13_4"),
        ("IntakeSurvey", "QID13_5"), ("IntakeSurvey", "QID13_6r"),
        ("IntakeSurvey", "QID13_7"), ("IntakeSurvey", "QID13_8r"),
        ("IntakeSurvey", "QID13_9"), ("IntakeSurvey", "QID13_10r"),
        ("IntakeSurvey", "QID13_11r"), ("IntakeSurvey", "QID13_12r"),
        ("IntakeSurvey", "QID13_13r"), ("IntakeSurvey", "QID13_14"),
        ("IntakeSurvey", "QID13_15r")]
}

# Competency variables
COMPETENCY_VARIABLES = ["walking_skill", "marking_skill", "transporting_skill"]

# ------------------------------------------------------------
# Here are the main functions used by the AC.

def initialize_state(config, reset_survey_vars_only=False):
    """
    Set the tracking values to their initial states. Should be called at the
    start of a trial + after end of a mission.
    """

    if reset_survey_vars_only:
        config.logger.info("Resetting survey variables only!")

        if len(config.state["player_list"]) == 0:
            config.logger.warn(
                "Cannot reset survey vars as there are no players...")
            return

        for player in config.state["player_list"]:
            for survey_var, _ in SURVEY_VARIABLES.items():
                config.state['players'][player][survey_var] = -1.0

        for survey_var, _ in SURVEY_VARIABLES.items():
            config.state['team'][f"{survey_var}_mean"] = -1.0
            config.state['team'][f"{survey_var}_sd"] = -1.0
        return

    config.logger.info("Resetting full state!")
    config.state = {
        # Map from alias to player name.
        'aliases': {},
        # List of players
        'player_list': [],

        # Set to True when a mission is running. We will accumulate + send
        # data prior to this being True
        'is_running': False,

        # # The last time we reported results to the bus.
        # 'last_report_time': -1,

        # Here we accumulate all of the msg_data we produce. When the mission
        # stops, we write these to a csv file.
        'msg_data': [],

        'team': {},
        'players': {},
        'comp_test_df': []
    }

    for survey_var, _ in SURVEY_VARIABLES.items():
        config.state['team'][f"{survey_var}_mean"] = -1.0
        config.state['team'][f"{survey_var}_sd"] = -1.0

    for comp_var in COMPETENCY_VARIABLES:
        config.state['team'][f"{comp_var}_mean"] = 0.0
        config.state['team'][f"{comp_var}_sd"] = 0.0

def record_aliases(data, config):
    """
    Find the aliases from the client info in the trial data and record them for
    later.
    """

    aliases = config.state['aliases']
    if len(aliases) != 0:
        config.logger.warn(
            "Aliases already exists. Resetting aliases")
        aliases = {}

    for client in data['client_info']:

        # Assume `playername` is in `client_info`. If it is not, then the format of
        # `client_info` has changed.
        if 'playername' not in client:
            config.logger.error("`playername` could not be found in `client_info`")
            continue

        playername = client['playername']
        if playername not in config.state['player_list']:
            config.state['player_list'].append(playername)

        for key in ('callsign', 'participant_id', 'participantid', 'uniqueid'):
            alias = client.get(key)
            if alias:
                aliases[alias] = playername

    config.logger.info(f'Prepared aliases: {aliases}')

def process_message(topic, data, config):
    """
    Records any ongoing state that will be used when producing results.
    """

    message_handler = MESSAGE_HANDLERS.get(topic)
    if message_handler is None:
        if topic not in config.unrecognized_topics:
            config.logger.warning(f'Unrecognized topic: {topic}')
            config.unrecognized_topics.add(topic)
        return

    message_handler(data, config)

    # If we are not running, just return without doing any work.
    # if not config.state['is_running']:
    #     return

# ------------------------------------------------------------
# Here are the functions for accumulating data during runtime.

def record_competency_variables(data, config):
    """
    Record competency variables
    """

    config.logger.debug(f"Message header: {config.msg_header}")
    config.logger.debug(f"Competency data: {data}")

    if len(data) == 0:
        config.logger.warn("Competency message is empty!")
        return

    if "task_message" not in data:
        config.logger.error("Competency msg data does not have `task_message`")
        return

    if "Competency" not in data['task_message']:
        return

    # assert "participant_id" in data
    if "playerName" not in data:
        config.logger.error("Competency msg data does not have `playerName`")
        return

    if "timestamp" not in config.msg_header:
        config.logger.error(
            "Competency header does not have a timestamp.")
        return

    config.state["comp_test_df"].append([
        config.msg_header['timestamp'],
        data['playerName'],
        data['task_message']])

def record_survey_variables(data, config):
    """
    Record survey variables
    """

    if len(data) == 0:
        config.logger.warn("Survey data is empty!")
        return

    data_ = json.loads(data["survey_response"]) if "survey_response" in data else data

    if "values" not in data_:
        config.logger.error('Survey data does not have values.')
        return

    player = get_player(data_["values"], config)
    player_data = ensure_player_data(player, config)

    survey_id = data_["values"]["surveyname"].lower()
    config.logger.info(f'Reading in survey results {survey_id} for player {player}')

    # Check if survey id is accurate and and survey is used
    if not ensure_survey(survey_id, config):
        return

    _, act_survey_name, _ = survey_id.split("_")
    for survey_var, qids in SURVEY_VARIABLES.items():
        config.logger.debug(f"Computing survey varible {survey_var}...")

        # if not ensure_survey_var_uses_survey(survey_id, survey_var, config):
        #     continue

        var_values = []
        if survey_var in ("rmie", ):
            var_values = \
                compute_count_survey_vars(act_survey_name, qids, data_, config)
        else:
            var_values = \
                compute_value_survey_vars(act_survey_name, qids, data_, config)
            # for _qid in qids:
            #     qid = _qid
            #     reverse = False
            #     if "r" in qid:
            #         qid = qid[0:qid.find("r")]
            #         reverse = True
            #     if not question_exists(qid, data_, config):
            #         continue
            #     var_val = data_["values"][qid] if not reverse else 8 - data_["values"][qid]
            #     config.logger.debug(f"QID {_qid} has value {var_val}")
            #     var_values.append(var_val)

        config.logger.debug(f"Values for {survey_var}: {var_values}")

        if len(var_values) > 0:
            value = float(np.mean(var_values)) if survey_var in ("rmie",) else np.mean(var_values)
            config.logger.debug(f"Survey variable {survey_var} = {value}")
            player_data[survey_var] = value

def record_role(data, config):
    """
    Record player role
    """

    player = get_player(data, config)
    player_data = ensure_player_data(player, config)
    player_data["role"] = data["new_role"]

MESSAGE_HANDLERS = {
    "observations/events/competency/task": record_competency_variables,
    "status/asistdataingester/surveyresponse": record_survey_variables,
    "observations/events/player/role_selected": record_role
}

# ------------------------------------------------------------
# And here is the function to pull all the runtime results together and publish
# our message to the message bus.

def publish_ac_result(data, config):
    """
    Prepares the score information and publishes a message on the bus.
    """
    msg_data = prepare_ac_msg_data(data, config)
    config.state['msg_data'].append(msg_data)

    # Round the scores to a reasonable amount of precision.
    round_values(msg_data)

    config.logger.debug(f"Sending the following message: {msg_data}")

    # Actually produce the message.
    config.helper.send_msg("agent/ac/" + \
                           config.helper.agent_name + "/beard",
                           "agent",
                           "AC:BEARD",
                           "0.1",
                           timestamp=config.helper.generate_timestamp(),
                           data=msg_data)

    config.logger.info(f' - data = {msg_data}')

def prepare_ac_msg_data(_data, config):
    """
    Prepares and returns the AC message data to be published for this period.
    """
    # elapsed_ms, delta_ms = get_elapsed_time(data, config)
    msg_data = {
        "team": config.state["team"]
    }
    msg_data.update(config.state["players"])

    # Compute all the supporting values.
    compute_competency_variables(msg_data, config)
    compute_survey_variables(msg_data, config)

    return msg_data

def compute_competency_variables(msg_data, config):
    """
    Computes characteristics of competency variables
    """

    ## INFO: Breakdown of each competency subtask
    # 1. Navigation subtask: time = (16+7*5) [tiles] * walking_skill [sec/tile]
    # 2. Role specific subtask:
    #     Medical_Specialist: time = 4 [victims] * saving_skill [sec/victim] + \
    #       (16+1+3+3+2) [tiles] * walking_skill [sec/tile]
    #     Engineering_Specialist: time = 8 [rubble] * digging_skill [sec/rubble] + \
    #       16 [tiles] * walking_skill [sec/tile]
    #     Transport_Specialist: time = 7 [detection] * detecting_skill [sec/detection] + \
    #       (16+5*4) [tiles] * walking_skill [sec/tile]
    # 3. Marker subtask: time = 6 [markers] * marking_skill [sec/marker] + \
    #       (16+1+3+3+3+3+2) [tiles] * walking_skill [sec/tile]
    # 4. Transport subtask: time = 9 [transporting] * transporting_skill [sec/transport] + \
    #       (16+8*3) [tiles] * walking_skill [sec/tile]
    ## INFO: we are only calculating values for common skills (only subtasks 1, 3, 4)

    if len(config.state["comp_test_df"]) == 0:
        config.logger.error("Competency data not found! Unable to compute competency variables!")
        return

    config.state["comp_test_df"] = pd.DataFrame(
        config.state["comp_test_df"],
        columns=["timestamp", "playername", "task_message"])

    # Sometimes there are multiple button hits leading to duplicate events
    config.state["comp_test_df"] = \
        config.state["comp_test_df"].sort_values(by=['playername','timestamp'])
    config.state["comp_test_df"] = \
        config.state["comp_test_df"].drop_duplicates(subset=['task_message'], keep='last')
    config.state["comp_test_df"] = config.state["comp_test_df"].reset_index(drop=True)

    # For each player, calculate values for each skill
    for player in config.state['player_list']:
        player_data = ensure_player_data(player, config)

        df = config.state["comp_test_df"].loc[config.state["comp_test_df"].playername == player]
        df = df.reset_index(drop=True)

        spent_time = [
             (pd.Timestamp(df.timestamp[i+1]) - pd.Timestamp(df.timestamp[i])).total_seconds() \
                 for i in range(len(df)-1)]

        if len(spent_time) < 1:
            config.logger.error(
                f"Player {player} did not fully complete competency test. "
                "Can not compute variables.")
            continue

        walking_skill = spent_time[0] / 51
        player_data['walking_skill'] = walking_skill

        if len(spent_time) < 3:
            config.logger.error(
                f"Player {player} did not fully complete competency test. "
                "Can not compute marking_skill or transporting_skill.")
            continue

        marking_skill = (spent_time[2] - 31 * walking_skill) / 6
        player_data['marking_skill'] = marking_skill

        if len(spent_time) < 4:
            config.logger.error(
                f"Player {player} did not fully complete competency test. "
                "Can not compute transporting_skill.")
            continue

        transporting_skill = (spent_time[3] - 40 * walking_skill) / 9
        player_data['transporting_skill'] = transporting_skill

    # Calculate mean and standard deviation of player skill values for the team
    compute_variables(COMPETENCY_VARIABLES, msg_data, config)

def compute_survey_variables(msg_data, config):
    """
    Computes characteristics of survey variables
    """

    # Compute survey variables for team
    compute_variables(list(SURVEY_VARIABLES.keys()), msg_data, config)

# ------------------------------------------------------------
# Support functions

def compute_value_survey_vars(act_survey_name, qids, data, config):
    """
    Compute survey variable based on value
    """

    var_values = []
    debug_values = []
    for exp_survey_name, _qid in qids:
        if not ensure_same_survey(exp_survey_name.lower(), act_survey_name, config):
            continue

        qid = _qid
        reverse = False
        if "r" in qid:
            qid = qid[0:qid.find("r")]
            reverse = True
        if not question_exists(qid, data, config):
            continue
        var_val = data["values"][qid] if not reverse else 8 - data["values"][qid]
        config.logger.debug(f"QID {_qid} has value {var_val}")
        var_values.append(var_val)

        debug_values.append({
            "QID": _qid,
            "Expected Value": data["values"][qid],
            "Actual Value":  var_val,
            "Is Reverse": reverse})

    config.logger.debug(
        f"Value-based values: {debug_values} - {sum(var_values)} - {len(debug_values)}")

    return var_values

def compute_count_survey_vars(act_survey_name, qids, data, config):
    """
    Count survey variable with an expected value
    """

    var_values = []
    debug_values = []
    for exp_survey_name, _qid, correct_val in qids:
        if not ensure_same_survey(exp_survey_name.lower(), act_survey_name, config):
            continue

        if not question_exists(_qid, data, config):
            continue

        var_val = 1 if data["values"][_qid] == correct_val else 0
        var_values.append(var_val)

        config.logger.debug(
            f"QID {_qid}, Expected val: {correct_val}, "
            f"Actual val: {data['values'][_qid]}, Is Equal: {var_val}")

        debug_values.append({
            "QID": _qid,
            "Expected Value": correct_val,
            "Actual Value":  data["values"][_qid],
            "Is Equal": var_val})

    config.logger.debug(
        f"Count-based values: {debug_values} - {sum(var_values)} - {len(debug_values)}")

    return var_values

def ensure_same_survey(exp_survey_name: str, act_survey_name: str, config):
    """
    True if survey variable uses survey. False otherwise
    """

    if exp_survey_name != act_survey_name:
        config.logger.debug(
            f"Survey {exp_survey_name} was expected. Got {act_survey_name}. Ignoring...")
        return False
    return True

# def ensure_survey_var_uses_survey(survey_id: str, survey_var: str, config):
#     """
#     True if survey variable uses survey. False otherwise
#     """

#     _, survey_name, _ = survey_id.split("_")
#     vars_to_surveys = config.extra_info["survey_vars_to_surveys"]

#     if survey_var not in vars_to_surveys:
#         config.logger.warn("Survey variable not available. Ignoring...")
#         return False

#     if survey_name not in vars_to_surveys[survey_var]:
#         config.logger.debug(
#             f"Survey var {survey_var} does not use {survey_name}. Ignoring...")
#         return False
#     return True

def ensure_survey(survey_id: str, config):
    """
    True if survey id is accurate and used. False otherwise
    """

    split_survey_name = survey_id.split("_")
    if len(split_survey_name) != 3:
        config.logger.warn(
            f"Survey {survey_id} does not have \"section_survey_study\" format. Ignoring...")
        return False

    section_name, survey_name, study_name = split_survey_name

    if study_name not in config.extra_info["section_survey_map"]:
        config.logger.warn(
            f"Study {study_name} does not exist. "
            "Please add to ConfigFolder/extraInfo.json")
        return False

    if section_name not in config.extra_info["section_survey_map"][study_name]:
        config.logger.warn(
            f"Section {section_name} does not exist for {study_name}. "
            "Please add to ConfigFolder/extraInfo.json")
        return False

    expected_survey_name = config.extra_info["section_survey_map"][study_name][section_name]
    if expected_survey_name != survey_name:
        config.logger.warn(
            f"Section {section_name} does not map to survey {survey_name}. "
            f"Expected Survey: {expected_survey_name}, Actual Survey: {survey_name}")
        return False

    # if full_survey_name not in \
    #   ("SectionA_TrainingKnowledge_Study3", "SectionD_IntakeSurvey_Study3"):
    # if full_survey_name not in \
    #   ("Section0_IntakeSurvey_Study3", "Section1_TrainingKnowledge_Study3"):

    if survey_id not in config.extra_info["allowed_survey_names"]:
        config.logger.warn(f"Survey {survey_id} is not used. Ignoring...")
        return False

    return True

def question_exists(qid: int, data, config):
    """
    True if a question-answer pair exists in the data. False otherwise.
    """

    if qid not in data["values"]:
        # QID is most likely in another survey or doesn't exist.
        return False

    if int(data["values"][qid]) == -99:
        # QID exists, but is not answered
        config.logger.warn(f"QID {qid} has missing answer (-99). Ignoring...")
        return False

    return True

def compute_variables(variables, msg_data, config):
    """
    Helper function for computing survey/competency variables for team
    """
    num_players = len(config.state["player_list"])
    for var in variables:
        var_values = []
        for player_id, player_data in config.state["players"].items():
            value = player_data[var]
            if value < 0.0 and var not in COMPETENCY_VARIABLES:
                # Competency skill variables can be negative; Survey variables cannot
                config.logger.warn(
                    f"Variable {var} is not set for player {player_id}.")
                continue
            var_values.append(value)

        if len(var_values) < num_players:
            config.logger.warn(
                f"Team consists of {num_players} players, but data "
                f"found for {len(var_values)} players for variable {var}")

        if len(var_values) > 0:
            msg_data["team"][f"{var}_mean"] = np.mean(var_values)
            msg_data["team"][f"{var}_sd"] = np.std(var_values)

def to_csv(config):
    """
    Save message data to CSV file
    """

    dataframe = []
    for msg_id, msg in enumerate(config.state["msg_data"]):
        for player_id, player_data in msg.items():
            for var, value in player_data.items():
                dataframe.append([msg_id, player_id, var, value])
    dataframe = pd.DataFrame(dataframe, columns=["Message ID", "Entity", "Variable", "Value"])
    dataframe.to_csv(f"{config.results_dir}/msg-data.csv")

def round_values(msg_data):
    """
    Round the values to a uniform (and not excessive) number of decimal places.
    """
    for key_1, json_obj in msg_data.items():
        if isinstance(json_obj, dict):
            for key_2, val in json_obj.items():
                if isinstance(val, float) and abs(val) < sys.float_info.epsilon:
                    # Cannot round 0.0
                    continue
                if isinstance(val, float):
                    val = round(val, NUM_SIG_FIGS - 1 - int(np.floor(np.log10(abs(val)))))
                    msg_data[key_1][key_2] = val

def get_player(data, config):
    """
    Returns the participant ID from the data. Falls back to playername or other
    as needed.
    """
    # If we were passed a message, step down into the data.
    if 'data' in data:
        data = data['data']

    if 'participant_id' in data:
        name = data['participant_id']
    elif 'participantid' in data:
        name = data.get("participantid")
    else:
        name = data.get('playername')

    aliases = config.state['aliases']
    if name in aliases:
        name = aliases[name]

    return name

def ensure_player_data(player, config):
    """
    Makes sure the player is recorded in the config. Return the player data
    structure.
    """
    if player not in config.state['players']:
        config.state['players'][player] = {'role': None}

        for survey_var, _ in SURVEY_VARIABLES.items():
            config.state['players'][player][survey_var] = -1.0

        for comp_var in COMPETENCY_VARIABLES:
            config.state['players'][player][comp_var] = 0.0

    return config.state['players'][player]
