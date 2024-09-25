# autopep8: off
import time
import rospy
import sys
import os

sys.path.append(os.getcwd())

# change this
import ros_nodes.joystick_node_test.main as joystick_node_test
# autopep8: on


# change this
_NODE_DELAY = 0.01  # 10ms delay / operation frequency 100Hz


if __name__ == '__main__':
    # change this
    joystick_node_test.ros_node_setup()

    while True:
        if rospy.is_shutdown():
            break

        try:
            # change this
            joystick_node_test.ros_node_loop()

        except rospy.ROSInterruptException:
            break

        time.sleep(_NODE_DELAY)
