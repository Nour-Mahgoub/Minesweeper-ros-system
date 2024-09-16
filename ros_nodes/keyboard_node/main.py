import rospy
import std_msgs.msg as ros_std_msgs
import sys
import pygame

import lib.ros as ros_man
import lib.settings as set_man

# module config
_NODE_NAME = 'keyboard_node'

# Define key mappings
_KEY_MAP = {
    pygame.K_w: 'w',
    pygame.K_a: 'a',
    pygame.K_s: 's',
    pygame.K_d: 'd',
    pygame.K_x: 'x',
    pygame.K_1: '1',
    pygame.K_2: '2',    
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_LCTRL: 'LT',
    pygame.K_RCTRL: 'RT',
    pygame.K_LSHIFT: 'LB',
    pygame.K_RSHIFT: 'RB'
}
 
# module state
_settings_obj: dict = None
_cmd_pub: rospy.Publisher = None

def ros_node_setup():
    global _settings_obj
    global _cmd_pub

    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = set_man.get_settings()
    q_size: int = _settings_obj['ros']['msg_queue_size']

    cmd_topic_id = ros_man.create_topic_id('cmd')

    _cmd_pub = rospy.Publisher(
        cmd_topic_id, ros_std_msgs.String, queue_size=q_size)

    pygame.init()
    pygame.display.set_mode((600, 400))  # Create a 1x1 pixel window


def ros_node_loop():

    
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print('key pressed')
            if event.key in _KEY_MAP:
                print(event.key)
                _cmd_pub.publish(_KEY_MAP[event.key])

if __name__ == '__main__':
    ros_node_setup()
    while True:
        ros_node_loop()