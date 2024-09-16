import pygame
import time
import serial
import rospy
import std_msgs.msg as ros_std_msgs
import sys

import lib.ros as ros_man
import lib.settings as set_man

_NODE_NAME = 'joystick_node'

# Initialize serial communication (adjust '/dev/ttyACM0' if necessary)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)

# Initialize pygame and the joystick module
pygame.init()
pygame.joystick.init()

# Detect if there are joysticks connected
if pygame.joystick.get_count() == 0:
    print("No joysticks connected.")
    exit()
else:
    # Get the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Joystick detected: {joystick.get_name()}")
    print(f"Number of buttons: {joystick.get_numbuttons()}")

# Main loop to capture joystick button presses and send serial commands
try:
    while True:
        pygame.event.pump()  # Ensure pygame processes events

        # Default command is 'x' (stop) if no button is pressed
        command = 'x'

        # Check for specific button presses and assign commands
        if joystick.get_button(0):  # Button 0 -> Forward ('w')
            command = 'w'
        elif joystick.get_button(1):  # Button 1 -> Right ('d')
            command = 'd'
        elif joystick.get_button(2):  # Button 2 -> Backward ('s')
            command = 's'
        elif joystick.get_button(3):  # Button 3 -> Left ('a')
            command = 'a'

        # Send the command via serial to the robot
        ser.write(command.encode())
        print(f"Sending: {command}")

        # Optional: Read response from Arduino (if any), ignoring errors
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        if response:
            print(f"Received from Arduino: {response}")

        # Small delay to avoid overwhelming the Arduino with too many commands
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Exiting...")

# Close the serial port and quit pygame when the script ends
ser.close()
pygame.quit()