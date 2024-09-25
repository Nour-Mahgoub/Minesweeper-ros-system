import rospy
from sensor_msgs.msg import Joy

def joystick_callback(data):
    # Process joystick data here
    print(data)

def main():
    rospy.init_node('joystick_subscriber')
    rospy.Subscriber('/joy', Joy, joystick_callback)
    rospy.spin()

if __name__ == '__main__':
    main()