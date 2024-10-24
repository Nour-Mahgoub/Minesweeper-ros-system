import rospy
import std_msgs.msg as ros_std_msgs
import lib.serial_driver as serial_driver
import sys



import lib.ros as ros_man
import lib.settings as set_man

_NODE_NAME = 'localisation_node'
_sensors_readings: rospy.Subscriber = None

def _sensors_readings_handler(msg: ros_std_msgs.String):
    #taking the data and splitting the sesnors data (2 IMUs and the coil)
    print(f"sensors data: {msg.data}")
    sensorsReadings=msg.data.split(',')
    IMU1=sensorsReadings[0:2]
    IMU2=sensorsReadings[3:5]
    coil=sensorsReadings[-1]
    #sensor fusion

def ros_node_setup():
    global _sensors_readings

    is_init = ros_man.init_node(_NODE_NAME)
    if not is_init:
        sys.exit()

    _settings_obj = set_man.get_settings()
    q_size: int = _settings_obj['ros']['msg_queue_size']
    topic_id=ros_man.compute_topic_id('sensors')

    _sensors_readings=rospy.Subscriber(
                topic_id, ros_std_msgs.String, _sensors_readings_handler)

def ros_node_loop():
    pass