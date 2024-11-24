import pygame
import time
import serial
import rospy
import std_msgs.msg as ros_std_msgs
import lib.serial_driver as serial_driver
import sys
import json
import threading


import lib.ros as ros_man
import lib.settings as set_man

_NODE_NAME = 'serial_node_test'
_cmd_joystick: rospy.Subscriber = None
_sensors_pub: rospy.Publisher = None

acm = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
usb = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
acm.flush()
usb.flush()

#time.sleep(2)
print("You're connected to the arduino")

# Function to read from the Arduino and publish it as a ROS message
# def read_from_arduino():
#     while not rospy.is_shutdown():
#         if ser.in_waiting > 0:  # Check if there is data waiting in the serial buffer
#             try:
#                 arduino_data = ser.readline().decode('utf-8').strip()  # Read and decode the data
#                 print(f"Received from Arduino on serial1: {arduino_data}")
                
#                 # You can publish this data to a ROS topic if necessary
#                 arduino_pub.publish(arduino_data)

#             except Exception as e:
#                 print(f"Error reading from Arduino on serial1: {e}")
#         time.sleep(0.01)  # Slight delay to avoid hogging the CPU

def _joystick_read_handler(msg: ros_std_msgs.String):
    # out_serial_packet = f"0000,0000,0000,0000,{msg.data}"
    print("in joystick handler")
    if not usb.is_open:
        usb.open()
    # ser.write((msg.data + '\n').encode())
    
    print(f"sent to arduino on serial2: {msg.data}")
  
    usb.write(msg.data.encode())
    print(f"sent already to arduino on serial2: {msg.data}")
    time.sleep(0.01)
    #print(type(msg.data))
    # time.sleep(1)
      # Lower the timeout
    # ser.open()
    # if ser.is_open:
    #     ser.write((command + '\n').encode())
    #     time.sleep(1)
    # else:
    #     ser.open()
    #     print("trying to open open")

    
    # ser.write(msg.data.encode())
    #time.sleep(0.01)
    #
    #ser.close()
    #serial_driver.write_raw((command).encode('ascii'))
    # ser.write(b"w\n")
    # time.sleep(1)
      # Lower the timeout
    # ser.open()
    # if ser.is_open:
    #     ser.write((command + '\n').encode())
    #     time.sleep(1)
    # else:
    #     ser.open()
    #     print("trying to open open")

    # Send the command continuously as long as the key is pressedser.write((command + '\n').encode())
    #ser.write((command+ '\n').encode('utf-8'))
    #ser.write(("hello").encode())
   # print(f"Sending: {command}")
    # Optional: Read response from Arduino (if any)
    # Reduce the delay
   # time.sleep(0.01)  # Reduce the sleep time to 10 ms
    #serial_driver.write_raw(msg.data)


def ros_node_setup():
    global _settings_obj
    global _cmd_joystick
    global _imu_pub
    global _encoder_pub
    is_init = ros_man.init_node(_NODE_NAME)
    #serial_driver.init_driver(1)
    

    if not is_init:
        sys.exit()
        


    _settings_obj = set_man.get_settings()
    q_size: int = _settings_obj['ros']['msg_queue_size']
    #time.sleep(0.1)
    _cmd_joystick=rospy.Subscriber(
                '/joystick_node_test/joystick_test', ros_std_msgs.String, _joystick_read_handler)
    
    imu_id = ros_man.create_topic_id('/imu/data')
    encoder_id = ros_man.create_topic_id('/odom')
    q_size: int = _settings_obj['ros']['msg_queue_size']

    _imu_pub = rospy.Publisher(
        imu_id, ros_std_msgs.String, queue_size=q_size)

    _encoder_pub = rospy.Publisher(
        encoder_id, ros_std_msgs.String, queue_size=q_size)

    
    # arduino_topic_id = ros_man.create_topic_id('arduino_data')
    # # Publisher for data read from the Arduino
    # arduino_pub = rospy.Publisher(arduino_topic_id, ros_std_msgs.String, queue_size=q_size)

    # # Start the thread to continuously read data from the Arduino
    # arduino_read_thread = threading.Thread(target=read_from_arduino)
    # arduino_read_thread.start()
def ros_node_loop():
    # try:
    #     if usb.in_waiting > 0:
    #             data = usb.readline().decode('utf-8').strip()
    #             print(f"Received sensor data: {data}")
    #             return data
    # except Exception as e:
    #     print(f"Error receiving sensor data: {e}")
        #if acm.in_waiting > 0:  # Check if there is data waiting in the serial buffer
    if not acm.is_open:
        acm.open()

         
        #print("we have data")
    arduino_data = acm.readline().decode('utf-8').strip().split()  # Read and decode the data
        #print(f"Received from Arduino on serial1: {arduino_data}")
                        
                        # You can publish this data to a ROS topic if necessary
                        
    _imu_pub.publish(arduino_data[0])
    _encoder_pub.publish(arduino_data[1])

            # except Exception as e:
            #     print(f"Error reading from Arduino on serial1: {e}")
            #time.sleep(0.01)  # Slight delay to avoid hogging the CPU
    


acm.close()
usb.close()
# def close_serial():
#     if ser.is_open:
#         ser.close()
#     print("Serial connection closed.")

#     topic_id = ros_man.create_topic_id('sensors')
#     q_size: int = _settings_obj['ros']['msg_queue_size']

#     _sensors_pub = rospy.Publisher(
#         topic_id, ros_std_msgs.String, queue_size=q_size)
      
#def ros_node_loop():
    #while True:
    # Read user input
        #command = input("Enter command: ").strip()

        # Exit the loop if the user types 'exit'
        #if command.lower() == 'exit':
           # break
       # command = ros_std_msgs.String
        # Send the command to Arduino
        #ser.write((command + '\n').encode())
        #print(f"Sent: {command}")

        # Optional: Read response from Arduino
        #response = ser.readline().decode('utf-8').strip()
        
        #if response:
            #print(f"Received from Arduino: {response}")

# def ros_node_loop():
#     # serial_input = serial_driver.read_raw()

#     # if serial_input != '':
#     #     acc_x = 0
#     #     acc_y = 0
#     #     acc_z = 0
#     #     coil = int(serial_input)
#     acc_x=ser.readline()
#     print(acc_x)

#         # publish serial data in ROS
#     _sensors_pub.publish(json.dumps({
#             'acc_x': acc_x,
#             # 'acc_y': acc_y,
#             # 'acc_z': acc_z,
#             # 'coil': coil,
#         }))


#ser2.close()
# Close the serial port
#close_serial()

