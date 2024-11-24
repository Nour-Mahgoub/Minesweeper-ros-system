#!/usr/bin/env python

import os
import subprocess
import rospy
import lib.ros as ros_man
import lib.settings as set_man

_NODE_NAME = 'ekf_runner'
global _settings_obj
_settings_obj = set_man.get_settings()

def run_ekf():
    rospy.init_node("ekf_runner", anonymous=True)

    # Path to the ekf configuration file
    ekf_config_path = os.path.abspath("./config/ekf_config.yaml")

    # Command to run the ekf node
    ekf_command = [
        "rosrun",
        "robot_localization",
        "ekf_localization_node",
        "_config_file:=" + ekf_config_path
    ]

    try:
        # Run the command
        subprocess.run(ekf_command, check=True)
    except subprocess.CalledProcessError as e:
        rospy.logerr(f"Error running EKF node: {e}")
    except FileNotFoundError:
        rospy.logerr("Ensure robot_localization is installed and in the ROS workspace!")

if __name__ == "_main_":
    is_init = ros_man.init_node(_NODE_NAME)
    #serial_driver.init_driver(1)

    if not is_init:
        sys.exit()
    run_ekf()