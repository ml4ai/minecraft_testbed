from ..models.jags import asist_jags as aj
from ..models.joint_activity_model import JointActivityModel
from ..views import jag_view, team_view

red_model = JointActivityModel(aj.ASIST_JAGS)
green_model = JointActivityModel(aj.ASIST_JAGS)
blue_model = JointActivityModel(aj.ASIST_JAGS)

regular = red_model.create(aj.RESCUE_REGULAR_VICTIM['urn'], {'victim-id': 27}, {})
regular.update_awareness('red', 'red', 1.0, 1000)
determine_victim_destination = regular.get_by_urn(aj.DETERMINE_VICTIM_DESTINATION['urn'], regular.inputs, regular.outputs)
determine_victim_destination.update_completion_status('red', True, 1500)
heal_victim = regular.get_by_urn(aj.HEAL_VICTIM['urn'], regular.inputs, regular.outputs)
heal_victim.update_completion_status('red', True, 8000)
pick_up_victim = regular.get_by_urn(aj.PICK_UP_VICTIM['urn'], regular.inputs, regular.outputs)
pick_up_victim.update_completion_status('red', True, 9000)
drop_off_victim = regular.get_by_urn(aj.DROP_OFF_VICTIM['urn'], regular.inputs, regular.outputs)
drop_off_victim.update_addressing('red', 'red', 1.0, 9000)

critical = red_model.create(aj.RESCUE_CRITICAL_VICTIM['urn'], {'victim-id': 31}, {})
critical.update_awareness('red', 'red', 1.0, 3000)
# critical.update_addressing('red', 'green', 0.5, 3000)
# critical.update_awareness('red', 'red', 1.0, 1000)
#
# critical2 = red_model.create(aj.RESCUE_CRITICAL_VICTIM['urn'], {'victim-id': 31}, {})
# critical2.update_awareness('red', 'green', 1.0, 3000)
# critical2.update_addressing('red', 'green', 0.5, 3000)
# critical2.update_awareness('red', 'red', 1.0, 1000)
#
regular2 = red_model.create(aj.RESCUE_REGULAR_VICTIM['urn'], {'victim-id': 19}, {})
regular2.update_awareness('red', 'red', 1.0, 6000)
# regular2.update_awareness('red', 'blue', 1.0, 4000)
#
#
# regular22 = blue_model.create(aj.RESCUE_REGULAR_VICTIM['urn'], {'victim-id': 19}, {})
# regular22.update_awareness('red', 'blue', 1.0, 4000)
# regular22.update_awareness('red', 'red', 1.0, 6000)
#
regular3 = red_model.create(aj.RESCUE_REGULAR_VICTIM['urn'], {'victim-id': 4}, {})
regular3.update_awareness('red', 'red', 1.0, 8000)
regular3.update_addressing('red', 'red', 0.0, 9000)
regular3.update_completion_status('red', True, 9000)
#
# regular4 = blue_model.create(aj.RESCUE_REGULAR_VICTIM['urn'], {'victim-id': 8}, {})
# regular4.update_awareness('blue', 'blue', 1.0, 12000)
# regular4.update_addressing('blue', 'blue', 1.0, 14000)

joint_activity_visualizer = team_view.TeamView(None)
jag_view_red = jag_view.JagView(joint_activity_visualizer.get_team_frame(), "red", red_model)
jag_view_green = jag_view.JagView(joint_activity_visualizer.get_team_frame(), "green", green_model)
jag_view_blue = jag_view.JagView(joint_activity_visualizer.get_team_frame(), "blue", blue_model)
jag_view_red.update()
jag_view_green.update()
jag_view_blue.update()
joint_activity_visualizer.add_jag_view("red", jag_view_red)
joint_activity_visualizer.add_jag_view("green", jag_view_green)
joint_activity_visualizer.add_jag_view("blue", jag_view_blue)
joint_activity_visualizer.mainloop()
