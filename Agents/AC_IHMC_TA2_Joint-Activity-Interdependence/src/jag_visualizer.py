import threading
import time

from .agents import joint_activity_client as jac
from .views import team_view


def print_summary():
    while True:
        joint_activity_client.team_summary()
        time.sleep(3.0)


joint_activity_client = jac.JointActivityClient()
joint_activity_client.start()

# polling_thread = threading.Thread(target=print_summary)
# polling_thread.start()

joint_activity_visualizer = team_view.TeamView(joint_activity_client)
joint_activity_visualizer.mainloop()



