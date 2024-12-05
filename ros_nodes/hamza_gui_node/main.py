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
import subprocess
import base64
import pickle


# module state
_settings_obj: dict = None
_cmd_pub: rospy.Publisher = None

# module config
_NODE_NAME = 'gui_node'

def ros_node_setup():
    global _settings_obj
    global _cmd_pub

    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()
    
    
    topic_id = ros_man.compute_topic_id(
        'camera_adapter_node', 'camera_feed')

    rospy.Subscriber(topic_id, ros_std_msgs.String, generate_frames)
############################################################

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



def generate_frames(msg: ros_std_msgs.String):
    input_bin_stream = msg.data.encode()

    # base64 decode
    decoded_bin_frame = base64.b64decode(input_bin_stream)

    # recover frame from binary stream
    frame = pickle.loads(decoded_bin_frame)

    # decode JPEG frame
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    while True:

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