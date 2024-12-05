import serial
import time




    # Open serial port (change '/dev/ttyACM0' if necessary)
ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)

    # Allow some time for the connection to establish
time.sleep(2)

print("Connected to Arduino. Type 'LED_ON' to turn the LED on, 'LED_OFF' to turn it off, or 'exit' to quit.")

while True:
    if not ser.is_open:
        ser.open()
        # Read user input
    command = input("Enter command: ").strip()

        # Exit the loop if the user types 'exit'
    if command.lower() == 'exit':
        break

        # Send the command to Arduino
    ser.write((command).encode())
    print(f"Sent: {command}")

        # Optional: Read response from Arduino
    #response = ser.readline().decode('utf-8').strip()
     #   if response:
      #      print(f"Received from Arduino: {response}")

    # Close the serial port
    ser.close()
