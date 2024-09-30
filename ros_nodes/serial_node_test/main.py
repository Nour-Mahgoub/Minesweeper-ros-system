import pygame
import time
import serial
import rospy
import std_msgs.msg as ros_std_msgs
import lib.serial_driver as serial_driver
import sys

import lib.ros as ros_man
import lib.settings as set_man

_NODE_NAME = 'serial_node_test'
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)

def _joystick_read_handler(msg: ros_std_msgs.String):
    # out_serial_packet = f"0000,0000,0000,0000,{msg.data}"
    print(msg.data)
    serial_driver.write_raw(msg.data)

time.sleep(2)

print("Connected to Arduino. Type 'LED_ON' to turn the LED on, 'LED_OFF' to turn it off, or 'exit' to quit.")

def ros_node_setup():
    global _settings_obj
    global _cmd_joystick
    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
            sys.exit()


    _settings_obj = set_man.get_settings()
    q_size: int = _settings_obj['ros']['msg_queue_size']

    _cmd_joystick = rospy.Subscriber(
        '/joystick_node_test/joystick_test', ros_std_msgs.String, _joystick_read_handler)

def ros_node_loop():
    while True:
    # Read user input
        #command = input("Enter command: ").strip()

        # Exit the loop if the user types 'exit'
       # if command.lower() == 'exit':
         #   break

        # Send the command to Arduino
        ser.write((command + '\n').encode())
        print(f"Sent: {command}")

        # Optional: Read response from Arduino
      #  response = ser.readline().decode('utf-8').strip()
       # if response:
            #print(f"Received from Arduino: {response}")

# Close the serial port
ser.close()