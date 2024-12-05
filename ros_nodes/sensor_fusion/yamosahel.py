# autopep8: off
import time
import rospy
import sys
import os

sys.path.append(os.getcwd())

# change this
import ros_nodes.sensor_fusion.run_ekf as sensor_fusion
# autopep8: on
import os
import subprocess
import rospy
import lib.ros as ros_man
import lib.settings as set_man

import sys

_NODE_NAME="sensor_fusion"
_NODE_DELAY = 0.01 

def run_ekf():
    is_init = ros_man.init_node('sensor_fusion')
    # serial_driver.init_driver(1)
    
    print(is_init)
    # if not is_init:
    #     sys.exit()
    # Path to the ekf configuration file
    # ekf_config_path = os.path.abspath("./config/ekf_config.yaml")
    # print(ekf_config_path)
    # # Command to run the ekf node
    # ekf_command = [
    #     "rosrun",
    #     "robot_localization",
    #     "ekf_localization_node",
    #     "_config_file:=" + ekf_config_path
    # ]

    # try:
    #     # Run the command
    #     subprocess.run(ekf_command, check=True)
    # except subprocess.CalledProcessError as e:
    #     rospy.logerr(f"Error running EKF node: {e}")
    # except FileNotFoundError:
    #     rospy.logerr("Ensure robot_localization is installed and in the ROS workspace!")

# if __name__ == '__main__':
#     # change this
    

#     while True:
#         if rospy.is_shutdown():
#             break

#         try:
#             # change this
#             sensor_fusion.run_ekf()

#         except rospy.ROSInterruptException:
#             break

#         time.sleep(_NODE_DELAY)

run_ekf()