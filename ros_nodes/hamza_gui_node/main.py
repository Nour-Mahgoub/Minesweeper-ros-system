# app.py
from flask import Flask, request, jsonify,render_template, Response
import cv2

#########ROS config###############
import lib.ros as ros_man
import lib.settings as set_man
import rospy
import lib.ros as ros_man
import lib.settings as set_man
import std_msgs.msg as ros_std_msgs
import sys
import os
import subprocess



# module state
_settings_obj: dict = None
_cmd_pub: rospy.Publisher = None

# module config
_NODE_NAME = 'keyboard_node'

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
    
############################################################

app = Flask(__name__)
#_camera_url = os.getenv('IP_CAMERA_URL')
_camera_url='http://192.168.1.2:8080/video'
cap = cv2.VideoCapture(_camera_url)

@app.route('/')
def index():
    return render_template('index.html')

# Capture key presses
@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    key = data.get('key')
    print(key)
    _cmd_pub.publish(key)
    return jsonify({'status': 'success'}), 200



def generate_frames():
    cap = cv2.VideoCapture(_camera_url)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in the correct format for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/data-statistics')
def data_statistics():

    data = {'Status': 'Still working On'}
    return jsonify(data)

@app.route('/api/node-info')
def node_info():
    topics = run_command('rostopic list')
    nodes = run_command('rosnode list')
    data = {
        'topics': topics,
        'nodes': nodes
    }
    return jsonify(data)

def run_command(command):
    """Run a shell command and return its output as a list of lines."""
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output.strip().split('\n')
    except subprocess.CalledProcessError as e:
        return [f"Error: {e}"]
    
@app.route('/api/command', methods=['POST'])
def command():
    command = request.form['command']
    output = run_command(command)
    return jsonify(output=output)