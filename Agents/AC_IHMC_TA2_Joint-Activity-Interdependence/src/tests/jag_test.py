from uuid import uuid4

from src.models.jags.jag import Jag
from src.models.joint_activity_model import JointActivityModel
from src.models.jags import asist_jags as aj
from src.models.player import Player
from src.utils.jag_utils import merge_jags


def _complete_check(jag_instance, inputs, player_id, elapsed_ms):
    check = jag_instance.get_by_urn(aj.CHECK_IF_UNLOCKED['urn'], inputs)
    check.update_addressing(player_id, player_id, 1.0, elapsed_ms)
    check.update_addressing(player_id, player_id, 0.0, elapsed_ms)
    check.update_completion_status(player_id, True, elapsed_ms)


def _complete_drop(jag_instance, inputs, player_id, prepare_time, address_time, completion_time, is_complete):
    check = jag_instance.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs)
    check.update_addressing(player_id, player_id, 1.0, address_time)
    check.update_addressing(player_id, player_id, 0.0, address_time)
    check.update_completion_status(player_id, is_complete, completion_time)


# print("*** TEST prepare update on addressing **********************************************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_check = red_player.joint_activity_model.create(aj.CHECK_IF_UNLOCKED['urn'], inputs_1)
# red_check.add_observer(red_player.notify)
# red_check.update_awareness(red_player.id, red_player.id, 1.0, 30400)
# red_check.update_addressing(red_player.id, red_player.id, 1.0, 35000)
# red_check.update_addressing(red_player.id, red_player.id, 0.0, 35000)
# red_check.update_completion_status(red_player.id, True, 35000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_check.to_string())
# print()

# print("*** TEST prepare update on addressing after first completion ****************************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_relocate = red_player.joint_activity_model.create(aj.RELOCATE_VICTIM['urn'], inputs_1)
# red_relocate.add_observer(red_player.notify)
# # print("test: red_relocate.update_awareness: 1.0, 30400")
# red_relocate.update_awareness(red_player.id, red_player.id, 1.0, 30400)
# # print(red_player.callsign + ": " + str(red_player.id))
# # print(red_relocate.to_string())
# red_pickup = red_relocate.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# print()
# print("test: red_pickup.update_addressing: 1.0, 42000")
# red_pickup.update_addressing(red_player.id, red_player.id, 1.0, 42000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
# print()
# print("test: red_pickup.update_addressing: 0.0, 42000")
# red_pickup.update_addressing(red_player.id, red_player.id, 0.0, 42000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
# print()
# print("test: red_pickup.update_completion_status: True, 42000")
# red_pickup.update_completion_status(red_player.id, True, 42000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
# red_drop_off = red_relocate.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# print()
# print("test: red_drop_off.update_addressing: 1.0, 42000")
# red_drop_off.update_addressing(red_player.id, red_player.id, 1.0, 42000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
# print()
# print("test: red_drop_off.update_addressing: 0.0, 42000")
# red_drop_off.update_addressing(red_player.id, red_player.id, 0.0, 54000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
# print()
# print("test: red_drop_off.update_completion_status: True, 42000")
# red_drop_off.update_completion_status(red_player.id, True, 54000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())

# print("*** TEST prepare update on addressing after first completion 3 layers deep *************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_relocate = red_player.joint_activity_model.create(aj.MOVE_VICTIM_TO_TRIAGE_AREA['urn'], inputs_1)
# red_relocate.add_observer(red_player.notify)
# red_relocate.update_awareness(red_player.id, red_player.id, 1.0, 30400)
# red_pickup = red_relocate.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# red_pickup.update_addressing(red_player.id, red_player.id, 1.0, 42000)
# red_pickup.update_addressing(red_player.id, red_player.id, 0.0, 42000)
# red_pickup.update_completion_status(red_player.id, True, 42000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
# red_drop_off = red_relocate.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# red_drop_off.update_addressing(red_player.id, red_player.id, 1.0, 42000)
# red_drop_off.update_addressing(red_player.id, red_player.id, 0.0, 54000)
# red_drop_off.update_completion_status(red_player.id, True, 54000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
# red_at = red_relocate.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
# red_at.update_addressing(red_player.id, red_player.id, 1.0, 55000)
# red_at.update_addressing(red_player.id, red_player.id, 0.0, 55000)
# red_at.update_completion_status(red_player.id, True, 55000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())

# print("*** TEST triage then pick up and place *************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_rescue = red_player.joint_activity_model.create(aj.RESCUE_VICTIM['urn'], inputs_1)
# red_rescue.add_observer(red_player.notify)
# red_rescue.update_awareness(red_player.id, red_player.id, 1.0, 30400)
#
# red_check = red_rescue.get_by_urn(aj.CHECK_IF_UNLOCKED['urn'], inputs_1)
# red_check.update_addressing(red_player.id, red_player.id, 1.0, 31000)
# red_check.update_addressing(red_player.id, red_player.id, 0.0, 31000)
# red_check.update_completion_status(red_player.id, True, 31000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_check.to_string())
#
# red_stabilize = red_rescue.get_by_urn(aj.STABILIZE['urn'], inputs_1)
# red_stabilize.update_addressing(red_player.id, red_player.id, 1.0, 32000)
# red_stabilize.update_addressing(red_player.id, red_player.id, 0.0, 35000)
# red_stabilize.update_completion_status(red_player.id, True, 35000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_stabilize.to_string())
#
# red_diagnose = red_rescue.get_by_urn(aj.DIAGNOSE['urn'], inputs_1)
# red_diagnose.update_addressing(red_player.id, red_player.id, 1.0, 32000)
# red_diagnose.update_addressing(red_player.id, red_player.id, 0.0, 33000)
# red_diagnose.update_completion_status(red_player.id, True, 33000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_diagnose.to_string())
#
# red_pickup = red_rescue.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# red_pickup.update_addressing(red_player.id, red_player.id, 1.0, 42000)
# red_pickup.update_addressing(red_player.id, red_player.id, 0.0, 42000)
# red_pickup.update_completion_status(red_player.id, True, 42000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_pickup.to_string())
#
# red_drop_off = red_rescue.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# red_drop_off.update_addressing(red_player.id, red_player.id, 1.0, 42000)
# red_drop_off.update_addressing(red_player.id, red_player.id, 0.0, 54000)
# red_drop_off.update_completion_status(red_player.id, True, 54000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_drop_off.to_string())
#
# red_at = red_rescue.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
# red_at.update_addressing(red_player.id, red_player.id, 1.0, 55000)
# red_at.update_addressing(red_player.id, red_player.id, 0.0, 55000)
# red_at.update_completion_status(red_player.id, True, 55000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_at.to_string())
#
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_rescue.to_string())

# print("*** TEST pick up and place then triage *************************")
client_info = {'participant_id': 'P000433', 'callsign': 'red'}
red_player = Player(client_info)
victim_type = 'regular'
victim_id = 35
inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
red_rescue = red_player.joint_activity_model.create(aj.RESCUE_VICTIM['urn'], inputs_1)
red_rescue.add_observer(red_player.notify)
red_rescue.update_awareness(red_player.id, red_player.id, 1.0, 30400)

red_check = red_rescue.get_by_urn(aj.CHECK_IF_UNLOCKED['urn'], inputs_1)
red_check.update_addressing(red_player.id, red_player.id, 1.0, 31000)
red_check.update_addressing(red_player.id, red_player.id, 0.0, 31000)
red_check.update_completion_status(red_player.id, True, 31000)
print(red_player.callsign + ": " + str(red_player.id))
print(red_check.to_string())

red_pickup = red_rescue.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
red_pickup.update_addressing(red_player.id, red_player.id, 1.0, 42000)
red_pickup.update_addressing(red_player.id, red_player.id, 0.0, 42000)
red_pickup.update_completion_status(red_player.id, True, 42000)
print(red_player.callsign + ": " + str(red_player.id))
print(red_pickup.to_string())

red_drop_off = red_rescue.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
red_drop_off.update_addressing(red_player.id, red_player.id, 1.0, 42000)
red_drop_off.update_addressing(red_player.id, red_player.id, 0.0, 54000)
red_drop_off.update_completion_status(red_player.id, True, 54000)
print(red_player.callsign + ": " + str(red_player.id))
print(red_drop_off.to_string())

red_stabilize = red_rescue.get_by_urn(aj.STABILIZE['urn'], inputs_1)
red_stabilize.update_addressing(red_player.id, red_player.id, 1.0, 32000)
red_stabilize.update_addressing(red_player.id, red_player.id, 0.0, 35000)
red_stabilize.update_completion_status(red_player.id, True, 35000)
print(red_player.callsign + ": " + str(red_player.id))
print(red_stabilize.to_string())

red_diagnose = red_rescue.get_by_urn(aj.DIAGNOSE['urn'], inputs_1)
red_diagnose.update_addressing(red_player.id, red_player.id, 1.0, 32000)
red_diagnose.update_addressing(red_player.id, red_player.id, 0.0, 33000)
red_diagnose.update_completion_status(red_player.id, True, 33000)
print(red_player.callsign + ": " + str(red_player.id))
print(red_diagnose.to_string())

red_pickup2 = red_rescue.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
red_pickup2.update_addressing(red_player.id, red_player.id, 1.0, 42000)
red_pickup2.update_addressing(red_player.id, red_player.id, 0.0, 42000)
red_pickup2.update_completion_status(red_player.id, True, 42000)
print(red_player.callsign + ": " + str(red_player.id))
print(red_pickup2.to_string())

red_drop_off2 = red_rescue.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
red_drop_off2.update_addressing(red_player.id, red_player.id, 1.0, 42000)
red_drop_off2.update_addressing(red_player.id, red_player.id, 0.0, 54000)
red_drop_off2.update_completion_status(red_player.id, True, 54000)
print(red_player.callsign + ": " + str(red_player.id))
print(red_drop_off2.to_string())

red_at = red_rescue.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
red_at.update_addressing(red_player.id, red_player.id, 1.0, 55000)
red_at.update_addressing(red_player.id, red_player.id, 0.0, 55000)
red_at.update_completion_status(red_player.id, True, 55000)
print(red_player.callsign + ": " + str(red_player.id))
print(red_at.to_string())

print(red_player.callsign + ": " + str(red_player.id))
print(red_rescue.to_string())

# # print("*** TEST merge 1 layer *************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_check = red_player.joint_activity_model.create(aj.CHECK_IF_UNLOCKED['urn'], inputs_1)
# red_check.add_observer(red_player.notify)
# red_check.update_awareness(red_player.id, red_player.id, 1.0, 30400)
# red_check.update_addressing(red_player.id, red_player.id, 1.0, 30400)
# red_check.update_addressing(red_player.id, red_player.id, 0.0, 30400)
# red_check.update_completion_status(red_player.id, True, 30400)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_check.to_string())
# print()
# green_client_info = {'participant_id': 'P000434', 'callsign': 'green'}
# green_player = Player(green_client_info)
# green_check = green_player.joint_activity_model.create(aj.CHECK_IF_UNLOCKED['urn'], inputs_1)
# green_check.add_observer(green_player.notify)
# green_check.update_awareness(green_player.id, green_player.id, 1.0, 41908)
# green_check.update_addressing(green_player.id, green_player.id, 1.0, 41908)
# green_check.update_addressing(green_player.id, green_player.id, 0.0, 41908)
# green_check.update_completion_status(green_player.id, True, 41908)
# print(green_player.callsign + ": " + str(green_player.id))
# print(green_check.to_string())
#
# print()
# merged_jag_1 = merge_jags(red_check, green_check)
# print("merged")
# print(merged_jag_1.to_string())
# print("completion: " + str(merged_jag_1.completion_duration()))

# # print("*** TEST merge 1 layer extra time *************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_pickup = red_player.joint_activity_model.create(aj.CHECK_IF_UNLOCKED['urn'], inputs_1)
# red_pickup.add_observer(red_player.notify)
# red_pickup.update_awareness(red_player.id, red_player.id, 1.0, 39000)
# red_pickup.update_addressing(red_player.id, red_player.id, 1.0, 46000)
# red_pickup.update_addressing(red_player.id, red_player.id, 0.0, 50000)
# red_pickup.update_completion_status(red_player.id, True, 50000)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_pickup.to_string())
# print()
# green_client_info = {'participant_id': 'P000434', 'callsign': 'green'}
# green_player = Player(green_client_info)
# green_pickup = green_player.joint_activity_model.create(aj.CHECK_IF_UNLOCKED['urn'], inputs_1)
# green_pickup.add_observer(green_player.notify)
# green_pickup.update_awareness(green_player.id, green_player.id, 1.0, 38000)
# green_pickup.update_addressing(green_player.id, green_player.id, 1.0, 42600)
# green_pickup.update_addressing(green_player.id, green_player.id, 0.0, 45000)
# green_pickup.update_completion_status(green_player.id, True, 45000)
# print(green_player.callsign + ": " + str(green_player.id))
# print(green_pickup.to_string())
#
# print()
# merged_jag_1 = merge_jags(red_pickup, green_pickup)
# print("merged")
# print(merged_jag_1.to_string())
# print("preparing: " + str(merged_jag_1.preparing_duration()))
# print("addressing: " + str(merged_jag_1.addressing_duration()))
# print("completion: " + str(merged_jag_1.completion_duration()))

# # print("*** TEST merge 3 layer *************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_relocate = red_player.joint_activity_model.create(aj.MOVE_VICTIM_TO_TRIAGE_AREA['urn'], inputs_1)
# red_relocate.add_observer(red_player.notify)
# red_relocate.update_awareness(red_player.id, red_player.id, 1.0, 34442)
# red_pickup = red_relocate.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# red_pickup.update_addressing(red_player.id, red_player.id, 1.0, 41691)
# red_pickup.update_addressing(red_player.id, red_player.id, 0.0, 54292)
# red_pickup.update_completion_status(red_player.id, True, 54292)
# red_drop_off = red_relocate.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# red_drop_off.update_addressing(red_player.id, red_player.id, 1.0, 54292)
# red_drop_off.update_addressing(red_player.id, red_player.id, 0.0, 67000)
# red_drop_off.update_completion_status(red_player.id, True, 67000)
# red_at = red_relocate.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
# red_at.update_addressing(red_player.id, red_player.id, 1.0, 66144)
# red_at.update_addressing(red_player.id, red_player.id, 0.0, 66144)
# red_at.update_completion_status(red_player.id, True, 66144)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
#
# green_client_info = {'participant_id': 'P000434', 'callsign': 'green'}
# green_player = Player(green_client_info)
# green_relocate = green_player.joint_activity_model.create(aj.MOVE_VICTIM_TO_TRIAGE_AREA['urn'], inputs_1)
# green_relocate.add_observer(green_player.notify)
# green_relocate.update_awareness(green_player.id, green_player.id, 1.0, 41908)
# green_pickup = green_relocate.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# green_pickup.update_addressing(green_player.id, green_player.id, 1.0, 42644)
# green_pickup.update_addressing(green_player.id, green_player.id, 0.0, 42644)
# green_pickup.update_completion_status(green_player.id, True, 42644)
# green_drop_off = green_relocate.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# green_drop_off.update_addressing(green_player.id, green_player.id, 1.0, 42644)
# green_drop_off.update_addressing(green_player.id, green_player.id, 0.0, 44946)
# green_drop_off.update_completion_status(green_player.id, True, 44946)
# green_at = green_relocate.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
# green_at.update_addressing(green_player.id, green_player.id, 1.0, 62000)
# green_at.update_addressing(green_player.id, green_player.id, 0.0, 62000)
# green_at.update_completion_status(green_player.id, True, 62000)
# print(green_player.callsign + ": " + str(green_player.id))
# print(green_relocate.to_string())
#
# print()
# merged_jag_1 = merge_jags(red_relocate, green_relocate)
# print("merged")
# print(merged_jag_1.to_string())
# print("preparing: " + str(merged_jag_1.preparing_duration()))
# print("addressing: " + str(merged_jag_1.addressing_duration()))
# print("completion: " + str(merged_jag_1.completion_duration()))

# # print("*** TEST merge 3 layer with one player incomplete *************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_relocate = red_player.joint_activity_model.create(aj.MOVE_VICTIM_TO_TRIAGE_AREA['urn'], inputs_1)
# red_relocate.add_observer(red_player.notify)
# red_relocate.update_awareness(red_player.id, red_player.id, 1.0, 34442)
# red_pickup = red_relocate.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# red_pickup.update_addressing(red_player.id, red_player.id, 1.0, 41691)
# red_pickup.update_addressing(red_player.id, red_player.id, 0.0, 54292)
# red_pickup.update_completion_status(red_player.id, True, 54292)
# red_drop_off = red_relocate.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# red_drop_off.update_addressing(red_player.id, red_player.id, 1.0, 54292)
# red_drop_off.update_addressing(red_player.id, red_player.id, 0.0, 67000)
# red_drop_off.update_completion_status(red_player.id, True, 67000)
# red_at = red_relocate.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
# red_at.update_addressing(red_player.id, red_player.id, 1.0, 66144)
# red_at.update_addressing(red_player.id, red_player.id, 0.0, 66144)
# red_at.update_completion_status(red_player.id, True, 66144)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
#
# green_client_info = {'participant_id': 'P000434', 'callsign': 'green'}
# green_player = Player(green_client_info)
# green_relocate = green_player.joint_activity_model.create(aj.MOVE_VICTIM_TO_TRIAGE_AREA['urn'], inputs_1)
# green_relocate.add_observer(green_player.notify)
# green_relocate.update_awareness(green_player.id, green_player.id, 1.0, 41908)
# green_pickup = green_relocate.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# green_pickup.update_addressing(green_player.id, green_player.id, 1.0, 42644)
# green_pickup.update_addressing(green_player.id, green_player.id, 0.0, 42644)
# green_pickup.update_completion_status(green_player.id, True, 42644)
# green_drop_off = green_relocate.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# green_drop_off.update_addressing(green_player.id, green_player.id, 1.0, 42644)
# green_drop_off.update_addressing(green_player.id, green_player.id, 0.0, 44946)
# green_drop_off.update_completion_status(green_player.id, True, 44946)
# # green_at = green_relocate.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
# # green_at.update_addressing(green_player.id, green_player.id, 1.0, 62000)
# # green_at.update_addressing(green_player.id, green_player.id, 0.0, 62000)
# # green_at.update_completion_status(green_player.id, True, 62000)
# print(green_player.callsign + ": " + str(green_player.id))
# print(green_relocate.to_string())
#
# print()
# merged_jag_1 = merge_jags(red_relocate, green_relocate)
# print("merged")
# print(merged_jag_1.to_string())
# print("preparing: " + str(merged_jag_1.preparing_duration()))
# print("addressing: " + str(merged_jag_1.addressing_duration()))
# print("completion: " + str(merged_jag_1.completion_duration()))

# print("*** TEST merge 3 layer with both players incomplete *************************")
# client_info = {'participant_id': 'P000433', 'callsign': 'red'}
# red_player = Player(client_info)
# victim_type = 'regular'
# victim_id = 35
# inputs_1 = {'victim-id': victim_id, 'victim-type': victim_type}
# red_relocate = red_player.joint_activity_model.create(aj.MOVE_VICTIM_TO_TRIAGE_AREA['urn'], inputs_1)
# red_relocate.add_observer(red_player.notify)
# red_relocate.update_awareness(red_player.id, red_player.id, 1.0, 34442)
# red_pickup = red_relocate.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# red_pickup.update_addressing(red_player.id, red_player.id, 1.0, 41691)
# red_pickup.update_addressing(red_player.id, red_player.id, 0.0, 54292)
# red_pickup.update_completion_status(red_player.id, True, 54292)
# red_drop_off = red_relocate.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# red_drop_off.update_addressing(red_player.id, red_player.id, 1.0, 54292)
# red_drop_off.update_addressing(red_player.id, red_player.id, 0.0, 67000)
# red_drop_off.update_completion_status(red_player.id, True, 67000)
# # red_at = red_relocate.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
# # red_at.update_addressing(red_player.id, red_player.id, 1.0, 66144)
# # red_at.update_addressing(red_player.id, red_player.id, 0.0, 66144)
# # red_at.update_completion_status(red_player.id, True, 66144)
# print(red_player.callsign + ": " + str(red_player.id))
# print(red_relocate.to_string())
#
# green_client_info = {'participant_id': 'P000434', 'callsign': 'green'}
# green_player = Player(green_client_info)
# green_relocate = green_player.joint_activity_model.create(aj.MOVE_VICTIM_TO_TRIAGE_AREA['urn'], inputs_1)
# green_relocate.add_observer(green_player.notify)
# green_relocate.update_awareness(green_player.id, green_player.id, 1.0, 41908)
# green_pickup = green_relocate.get_by_urn(aj.PICK_UP_VICTIM['urn'], inputs_1)
# green_pickup.update_addressing(green_player.id, green_player.id, 1.0, 42644)
# green_pickup.update_addressing(green_player.id, green_player.id, 0.0, 42644)
# green_pickup.update_completion_status(green_player.id, True, 42644)
# green_drop_off = green_relocate.get_by_urn(aj.DROP_OFF_VICTIM['urn'], inputs_1)
# green_drop_off.update_addressing(green_player.id, green_player.id, 1.0, 42644)
# green_drop_off.update_addressing(green_player.id, green_player.id, 0.0, 44946)
# green_drop_off.update_completion_status(green_player.id, True, 44946)
# # green_at = green_relocate.get_by_urn(aj.AT_PROPER_TRIAGE_AREA['urn'], inputs_1)
# # green_at.update_addressing(green_player.id, green_player.id, 1.0, 62000)
# # green_at.update_addressing(green_player.id, green_player.id, 0.0, 62000)
# # green_at.update_completion_status(green_player.id, True, 62000)
# print(green_player.callsign + ": " + str(green_player.id))
# print(green_relocate.to_string())
#
# print()
# merged_jag_1 = merge_jags(red_relocate, green_relocate)
# print("merged")
# print(merged_jag_1.to_string())
# print("preparing: " + str(merged_jag_1.preparing_duration()))
# print("addressing: " + str(merged_jag_1.addressing_duration()))
# print("completion: " + str(merged_jag_1.completion_duration()))
