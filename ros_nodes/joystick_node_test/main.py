import pygame
import time
import serial
import rospy
import std_msgs.msg as ros_std_msgs
import sys

import lib.ros as ros_man
import lib.settings as set_man

_NODE_NAME = 'joystick_node_test'
# ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
def ros_node_setup():
    global _settings_obj
    global joystick
    global _joystick_handler
    global _joystick_pub
    

    # Initialize serial communication (adjust '/dev/ttyACM0' if necessary)

    # Initialize pygame and the joystick module

    pygame.init()
    pygame.joystick.init()
    is_init = ros_man.init_node(_NODE_NAME)

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

        

        if not is_init:
            sys.exit()
        _settings_obj = set_man.get_settings()
        q_size: int = _settings_obj['ros']['msg_queue_size']

        joystick_topic_id = ros_man.create_topic_id('joystick_test')

        _joystick_pub = rospy.Publisher(
        joystick_topic_id, ros_std_msgs.String, queue_size=q_size)

# Main loop to capture joystick button presses and send serial commands
def ros_node_loop():
#     _previous_command='x'
#     command = 'x'
#     try:
#         while True:
#             pygame.event.pump()  # Ensure pygame processes events

#             # Default command is 'x' (stop) if no button is pressed
            

#             # Check for specific button presses and assign commands
#             if joystick.get_button(2):  # Button 0 -> Forward ('w')
#                 command = 'w'
#             elif joystick.get_button(1):  # Button 1 -> Right ('d')
#                 command = 'd'
#             elif joystick.get_button(0):  # Button 2 -> Backward ('s')
#                 command = 's'
#             elif joystick.get_button(3):  # Button 3 -> Left ('a')
#                 command = 'a'
#             # elif joystick.get_button(4):  # Button 4 -> ARM UP
#             #     command = 'au'
#             # elif joystick.get_button(5):  # Button 5 -> ARM DOWN
#             #     command = 'ad'
#             elif joystick.get_button(4):    #Button 11 -> stop
#                 command = 'x'

# #   # Check for events (e.g., joystick button presses, axis movements)
# #             for event in pygame.event.get():
# #                 if event.type == pygame.JOYBUTTONDOWN:
# #                     print("Button pressed:", event.button)
# #                 elif event.type == pygame.JOYBUTTONUP:
# #                     print("Button released:", event.button)
# #                 elif event.type == pygame.JOYAXISMOTION:
# #                     print("Axis moved:", event.axis, event.value)

# #         # Get axis values
# #             axis_x = joystick.get_axis(0)
# #             axis_y = joystick.get_axis(1)

#     # Do something with the axis values (e.g., control a robot, play a game)

#             pygame.event.pump()  # Update the event queue

#             if command != _previous_command:
                

#             # Send the command via serial to the robot
#             #ser.write(command.encode())
#                 print(f"Sending: {command}")
#                 _joystick_pub.publish(command)
#                 _previous_command=command
#             #_joystick_pub.publish(f"Sending: {axis_x} and {axis_y}")
#             # Optional: Read response from Arduino (if any), ignoring errors
#             # response = ser.readline().decode('utf-8', errors='ignore').strip()
#             # if response:
#             #     print(f"Received from Arduino: {response}")

#             # Small delay to avoid overwhelming the Arduino with too many commands
#             # time.sleep(0.01)

#     except KeyboardInterrupt:
#         print("Exiting...")
#######################################################################################################################
     try:
        while True:
            for event in pygame.event.get():  # Get events

               

                # Check for button press events (send specific command)
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 2:  # Button 0 -> Forward ('w')
                        command = 's'
                    elif event.button == 1:  # Button 1 -> Right ('d')
                        command = 'd'
                    elif event.button == 0:  # Button 2 -> Backward ('s')
                        command = 'w'
                    elif event.button == 3:  # Button 3 -> Left ('a')
                        command = 'a'
                    elif event.button == 5:  # Button 4 -> ARM UP
                        command = 'z'
                    elif event.button == 4:  # Button 5 -> ARM DOWN
                        command = 'c'
                    elif event.button == 7:
                        command = 'n'
                    elif event.button ==6:
                        command='m'
                    
                    else :
                        command='x'
                

                    # Send the command if a button is pressed
                    print(f"Sending: {command}")
                    _joystick_pub.publish(command)

                # Check for button release events (send stop 'x' command)
                elif event.type == pygame.JOYBUTTONUP:
                    print("Sending: x")
                    _joystick_pub.publish('x')

     except KeyboardInterrupt:
        print("Exiting...")

# Close the serial port and quit pygame when the script ends
#ser.close()
pygame.quit()