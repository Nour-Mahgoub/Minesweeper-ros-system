import os
import struct
import sys

# Open the /dev/input/mice device file
mouse_file = '/dev/input/mouse0'

try:
    with open(mouse_file, 'rb') as f:
        while True:
            # Read 3 bytes from the mouse device
            data = f.read(3)
            if len(data) < 3:
                break
            
            # Unpack the bytes into a tuple
            buttons, dx, dy = struct.unpack('BBB', data)

            # Print dx and dy values
            print(f'dx: {dx}, dy: {dy}')

except KeyboardInterrupt:
    # Gracefully exit on Ctrl+C
    print("Exiting...")
    sys.exit(0)
except Exception as e:
    print(f"An error occurred: {e}")
