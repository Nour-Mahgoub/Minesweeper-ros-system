import rospy
import std_msgs.msg as ros_std_msgs
import sys
import cv2
import base64
import pickle
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np

import lib.ros as ros_man

# Module config
_NODE_NAME = 'camera_reader_node'
script_dir = "/home/hamza/Minesweeper-ros-system/ros_nodes/camera_reader_node/"

# Global variables for frame handling
latest_frame = None
processed_frame = None
frame_lock = threading.Lock()
processed_frame_lock = threading.Lock()
executor = ThreadPoolExecutor(max_workers=1)  # Limit to one thread for MattMatt
future = None  # To keep track of MattMatt task

# Variables to store last displayed frames
last_displayed_frame = None
last_displayed_processed_frame = None

def MattMatt():
    try:
        # Define the directory where the shell script is located
        script_directory = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_directory)  # Change working directory to where the script is

        # Execute the command
        flag = os.system("./run_image.sh")
        flag= bool(flag)
        print(f'this is the flag for detection {flag}')
    except Exception as ex:
        print("Error executing the command:", ex)

# ROS message handler
def _ros_frame_reader(msg: ros_std_msgs.String):
    global latest_frame
    global frame_lock

    try:
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
        print("Received a frame.")
    except Exception as e:
        print("Error in _ros_frame_reader:", e)

def process_frame_timer(event):
    global latest_frame
    global frame_lock
    global future

    # Check if there's an ongoing task
    if future is not None and not future.done():
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

    # Submit MattMatt to run asynchronously
    future = executor.submit(run_mattmatt)

def run_mattmatt():
    global processed_frame
    try:
        print("Running MattMatt.")
        MattMatt()  # Run the shell script

        # Load the processed image from YOLO output (after MattMatt runs)
        out = cv2.imread("out.jpg")
        if out is not None:
            with processed_frame_lock:
                processed_frame = out.copy()
            print("Processed frame updated.")
        else:
            print("Processed image 'out.jpg' not found.")
    except Exception as ex:
        print("Model did not work:", ex)

def display_frames():
    global latest_frame
    global processed_frame
    global last_displayed_frame
    global last_displayed_processed_frame

    try:
        # Display latest_frame
        with frame_lock:
            if latest_frame is not None:
                last_displayed_frame = latest_frame.copy()
        if last_displayed_frame is not None:
            frame2 = cv2.resize(last_displayed_frame, (600, 600))
            cv2.imshow('Live_Camera_Feed', frame2)

        # Display processed_frame
        with processed_frame_lock:
            if processed_frame is not None:
                last_displayed_processed_frame = processed_frame.copy()
        if last_displayed_processed_frame is not None:
            processed_frame_resized = cv2.resize(last_displayed_processed_frame, (600, 600))
            cv2.imshow("Detections", processed_frame_resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            rospy.signal_shutdown("User requested shutdown.")
    except Exception as e:
        print("Error in display_frames:", e)

def ros_node_setup():
    is_init = ros_man.init_node(_NODE_NAME)
    if not is_init:
        sys.exit()

    topic_id = ros_man.compute_topic_id('camera_adapter_node', 'camera_feed')

    # Subscriber with queue_size=1 to only keep the latest frame
    rospy.Subscriber(topic_id, ros_std_msgs.String, _ros_frame_reader)

    # Set up a timer to process frames every second
    rospy.Timer(rospy.Duration(1), process_frame_timer)

def ros_spin_thread():
    rospy.spin()

if __name__ == '__main__':
    try:
        ros_node_setup()
        # Start ROS spin in a separate thread
        spin_thread = threading.Thread(target=ros_spin_thread)
        spin_thread.start()

        # Create windows before entering main loop
        cv2.namedWindow('Live_Camera_Feed', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Detections', cv2.WINDOW_NORMAL)

        while not rospy.is_shutdown():
            display_frames()
            # Sleep for a short time to allow ROS callbacks to process
            cv2.waitKey(1)
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        pass
