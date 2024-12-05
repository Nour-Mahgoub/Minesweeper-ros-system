# autopep8: off
import time
import rospy
import sys
import os

sys.path.append(os.getcwd())

# change this
import ros_nodes.sensor_fusion.main as sensor_fusion
# autopep8: on

import rospy
# change this
_NODE_DELAY = 0.01  # 10ms delay / operation frequency 100Hz


if __name__ == '__main__':
    # change this
    sensor_fusion.ros_node_setup()

    while True:
        if rospy.is_shutdown():
            break

        try:
            # change this
            sensor_fusion.ros_node_loop()

        except rospy.ROSInterruptException:
            break

        time.sleep(_NODE_DELAY)
