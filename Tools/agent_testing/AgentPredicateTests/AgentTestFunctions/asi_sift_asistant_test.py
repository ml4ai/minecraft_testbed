# This script was written by Aptima in May 2022 in advance of study 3. On 10
# May, Jeff Rye adjusted the tests to be more sophisticated and to make it
# possible to run them alone.
#
# You can run this on a metadata file as in:
# python3 ./asi_sift_asistant_test.py NotHSR_....metadata
#
"""
Implements the test criteria to verify that the SIFT agent is working.
"""

import argparse
import json
import sys

# (# status messages with state != "ok") = 0
# (# versioninfo messages with version = 0.4.0) > 0 per trial
# chat messages > 3

# Expected SIFT agent version.
TARGET_VERSION = '0.4.4'

# If the verbose flag is set, we'll log some extra stuff.
def asi_sift_asistant_test(name, lines, table:dict, verbose = False):
    """
    Performs the tests for the SIFT agent. Stores the test results in the table.
    """
    num_heartbeats_ok = 0
    num_heartbeats_error = 0
    version = ''
    num_chat_messages = 0
    num_sift_messages = 0
    num_test_errors = 0

    is_training_mission = True

    # To aid in debugging, we record all topics.
    topics = {}

    for line_num, line in enumerate(lines):
        try:
            # Parse the line.
            obj = json.loads(line)

            # No topic, no problem.
            topic = obj.get('topic', '')
            topic = topic.lower()

            # Increment the count for this topic.
            if topic not in topics:
                topics[topic] = 0
            topics[topic] += 1

            # Get the msg and data fields for use below. Default to empty
            # dictionaries if they are not present.
            msg = obj.get('msg', {})
            data = obj.get('data', {})

            if topic == 'trial':
                sub_type = msg.get('sub_type', '')
                sub_type = sub_type.lower()
                if sub_type == 'start':
                    mission = data.get('experiment_mission', '')
                    mission = mission.lower()
                    if mission.find("training") == -1:
                        is_training_mission = False

            if topic == 'agent/intervention/sift_asistant/chat':
                num_chat_messages += 1

            if topic == 'agent/sift_asistant/versioninfo':
                version = data.get('version')

            if topic == 'status/sift_asistant/heartbeats':
                state = data.get('state')
                status = data.get('status')
                if state == 'ok':
                    num_heartbeats_ok += 1
                elif state == 'error' and \
                    status not in (
                        # We see these when we handle unexpected victim and tool
                        # use events (e.g., putting down a victim twice). These
                        # are annoying but do *not* reflect agent failure.
                        'pop from empty list',
                        'list index out of range'
                    ):
                    num_heartbeats_error += 1

                    print(f'WARNING: Found SIFT heartbeat with state: {state}')
                    print(json.dumps(data, indent=2))

            if 'sift' in topic:
                num_sift_messages += 1

        except Exception as err:   # pylint: disable=broad-except
            print(f'Something went wrong on line: {line_num}')
            print(f'  {err}')
            num_test_errors += 1

    # Report some summary info if needed.
    if verbose:
        print('Topics')
        print(json.dumps(topics, indent=2))

    if num_test_errors:
        print(f'WARNING Encountered {num_test_errors} errors in testing script')

    # Now that we have accumulated the data, write the test results to the
    # global table. This is what will be reported to the file.
    #
    # - The key is the id of the test.
    # - The value is a tuple: [name, success, data, predicate]
    #   - name is the agent name
    #   - success is a string "True" or "False" reflecting pass or failure for
    #     this check
    #   - data is extra data you've given to accompany the result (e.g., the
    #     values used in the comparison),
    #   - a string with the pass criteria
    #

    # NOTE: We could *also* be making a check to see if we're the responsible
    # agent. But that would inhibit tests where multiple agents are run. So
    # let's not do that for now.
    if is_training_mission:
        print('This was training mission omitting SIFT results')
        return

    table[f'{name}_#_test_err'] = [
        name,
        str(num_test_errors == 0),
        f'num of errors caught in testing = {num_test_errors}',
        '# errors in test script = 0'
    ]
    table[f'{name}_#_sift_msgs'] = [
        name,
        str(num_chat_messages > 0),
        f'# of messages from SIFT agent = {num_sift_messages}',
        '# sift messages > 0'
    ]
    table[f'{name}_htbts_ok'] = [
        name,
        str(num_heartbeats_ok > 0),
        f'#_heartbeats_ok = {num_heartbeats_ok}',
        '# heartbeats with ok status > 0'
    ]
    table[f'{name}_htbts_err'] = [
        name,
        # Need to see some messages from our agent and we shouldn't see any
        # errors.
        str(num_sift_messages > 0 and num_heartbeats_error == 0),
        f'#_heartbeats_error = {num_heartbeats_error}',
        '# SIFT messages > 0 and # htbts w. err status == 0'
    ]
    table[f'{name}_correct_ver'] = [
        name,
        str(version == TARGET_VERSION),
        f'SIFT agent version = {version}',
        f'version = {TARGET_VERSION}'
    ]
    table[f'{name}_#_interventions'] = [
        name,
        str(num_chat_messages > 0),
        f'num interventions = {num_chat_messages}',
        '# interventions > 0'
    ]


# ------------------------------------------------------------
# This is the main function, used only when this script is run from the command
# line.

def main(args):
    """Main entry point for script."""
    # First prepare our configuration.
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',
                        dest='verbose',
                        action='store_true',
                        help='If set, print some additional logging detail ' +
                        'while testing the messages.')
    parser.add_argument('in_filename',
                        help='Metadata file containing MQTT messages as JSON ' +
                        'objects, one per line.')
    config = parser.parse_args(args)

    # Get the messages for us to test.
    print(f'Testing SIFT messages in: {config.in_filename}')
    with open(config.in_filename, 'rt', encoding='utf-8') as in_file:
        lines = in_file.readlines()
    print(f'Read {len(lines)} lines from input file')

    # This is where we'll store the results.
    table = {}

    # Actually do the testing.
    asi_sift_asistant_test('asi_sift_asistant_test', lines, table,
                           config.verbose)

    # All done testing, dump the results to stdout.
    print('Test results:')
    print(json.dumps(table, indent=2))

    # Report our passing rate.
    pass_count = 0
    total_count = 0
    for result in table.values():
        if result[1] == 'True':
            pass_count += 1
        total_count += 1
    percent = 100.0 * pass_count / total_count
    print(f'Passed {pass_count} of {total_count} tests -- {percent:.1f}%')

    # Return 0 if all tests succeeded, false otherwise.
    return 0 if pass_count == total_count else 1


# ------------------------------------------------------------
# This is the magic that runs the main function when this is invoked
# as a script.

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
