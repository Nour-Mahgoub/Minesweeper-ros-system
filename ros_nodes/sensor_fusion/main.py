import rospy
import sys
import std_msgs.msg as ros_std_msgs
import json
import os
import lib.ros as ros_man
import lib.settings as set_man
import subprocess


# module config
_NODE_NAME = 'sensor_fusion'

# module state
_sensors_pub: rospy.Publisher = None
_cmd_sub: rospy.Subscriber = None
_settings_obj: dict = None



def ros_node_setup():
    global _sensors_pub
    global _settings_obj
    global _cmd_sub

    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = set_man.get_settings()

    q_size: int = _settings_obj['ros']['msg_queue_size']




def ros_node_loop():
    is_init = ros_man.init_node('sensor_fusion')
    # serial_driver.init_driver(1)
    
    # print(is_init)
    if not is_init:
        sys.exit()
    # Path to the ekf configuration file
    ekf_config_path = os.path.abspath("./config/ekf_config.yaml")
    print(ekf_config_path)
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