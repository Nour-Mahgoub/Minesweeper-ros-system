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
_cmd_joystick: rospy.Subscriber = None
# ser = serial.Serial('/dev/ttyACM1', 9600, timeout=0.1)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
ser.flush()
#time.sleep(2)
print("You're connected to the arduino")


def _joystick_read_handler(msg: ros_std_msgs.String):
    # out_serial_packet = f"0000,0000,0000,0000,{msg.data}"
    
    if not ser.is_open:
         ser.open()
    # ser.write((msg.data + '\n').encode())
    
    print(f"sent to arduino : {msg.data}")
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

    
    ser.write(msg.data.encode())
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
    is_init = ros_man.init_node(_NODE_NAME)
    serial_driver.init_driver()
    

    if not is_init:
        sys.exit()
        


    _settings_obj = set_man.get_settings()
    q_size: int = _settings_obj['ros']['msg_queue_size']
    #time.sleep(0.1)
    _cmd_joystick=rospy.Subscriber(
                '/joystick_node_test/joystick_test', ros_std_msgs.String, _joystick_read_handler)
      
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

# Close the serial port
ser.close()


