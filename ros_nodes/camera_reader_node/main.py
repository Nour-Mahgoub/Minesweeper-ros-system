import rospy
import std_msgs.msg as ros_std_msgs
import sys
import cv2
import base64
import pickle
import os
import threading
import time

import lib.ros as ros_man

# Module config
_NODE_NAME = 'camera_reader_node'
script_dir = "/home/morshedy/Minesweeper-ros-system/ros_nodes/camera_reader_node/"

# Global variables for frame handling
latest_frame = None
frame_lock = threading.Lock()
mattmatt_running = False  # Flag to prevent overlapping runs

def MattMatt():
    try:
        # Define the directory where the shell script is located
        script_directory = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_directory)  # Change working directory to where the script is

        # Execute the command with sudo
        os.system("./run_image.sh")

    except Exception as ex:
        print("Error executing the command:", ex)

# ROS message handler
def _ros_frame_reader(msg: ros_std_msgs.String):
    global latest_frame
    global frame_lock

    input_bin_stream = msg.data.encode()

    # Base64 decode
    decoded_bin_frame = base64.b64decode(input_bin_stream)

    # Recover frame from binary stream
    frame = pickle.loads(decoded_bin_frame)

    # Decode JPEG frame
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Update the latest frame with thread safety
    with frame_lock:
        latest_frame = frame.copy()

    # Optionally, display the live camera feed
    frame2 = cv2.resize(frame, (1280, 720))
    cv2.imshow('Live Camera Feed', frame2)
    cv2.waitKey(1)

def process_frame_timer(event):
    global latest_frame
    global frame_lock
    global mattmatt_running

    # Prevent overlapping runs
    if mattmatt_running:
        print("MattMatt is still running. Skipping this frame.")
        return

    # Retrieve the latest frame
    with frame_lock:
        if latest_frame is None:
            print("No frame available to process.")
            return
        frame_to_process = latest_frame.copy()

    # Save the frame as 'frame.jpg'
    cv2.imwrite(os.path.join(script_dir, 'frame.jpg'), frame_to_process)

    # Start MattMatt in a separate thread
    threading.Thread(target=run_mattmatt).start()

def run_mattmatt():
    global mattmatt_running
    mattmatt_running = True
    MattMatt()  # Run the shell script

    try:
        # Load the processed image from YOLO output (after MattMatt runs)
        out = cv2.imread("out.jpg")
        if out is not None:
            cv2.imshow("Detections", out)
            cv2.waitKey(1)
        else:
            print("Processed image 'out.jpg' not found.")
    except Exception as ex:
        print("Model did not work:", ex)
    finally:
        mattmatt_running = False

def ros_node_setup():
    is_init = ros_man.init_node(_NODE_NAME)
    if not is_init:
        sys.exit()

    topic_id = ros_man.compute_topic_id('camera_adapter_node', 'camera_feed')

    # Subscriber with queue_size=1 to only keep the latest frame
    rospy.Subscriber(topic_id, ros_std_msgs.String, _ros_frame_reader)

    # Set up a timer to process frames every second
    rospy.Timer(rospy.Duration(1.0), process_frame_timer)

def ros_node_loop():
    rospy.spin()

if __name__ == '__main__':
    try:
        ros_node_setup()
        ros_node_loop()
    except rospy.ROSInterruptException:
        pass
