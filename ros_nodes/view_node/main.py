import rospy
import sys
import std_msgs.msg as ros_std_msgs
import json

import lib.ros as ros_man
import lib.settings as set_man


_NODE_NAME = 'serial_interface_node'

# module state
_cmd_sub: rospy.Subscriber = None
_settings_obj: dict = None


def _keyboard_cmd_read_handler(msg: ros_std_msgs.String):
    # out_serial_packet = f"0000,0000,0000,0000,{msg.data}"
    print(msg.data)


def ros_node_setup():
    global _cmd_sub
    global _settings_obj

    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = set_man.get_settings()


    _cmd_sub = rospy.Subscriber(
        '/keyboard_node/cmd', ros_std_msgs.String, _keyboard_cmd_read_handler)
    
def ros_node_loop():
    pass
