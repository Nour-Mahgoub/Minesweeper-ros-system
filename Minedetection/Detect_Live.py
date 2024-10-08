
import os
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('best.pt')  # Ensure 'best.pt' is the correct path to your YOLO model

# Open a connection to the webcam
cap = cv2.VideoCapture(0)  # 0 is typically the default webcam

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Loop to continuously get frames from the webcam
while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # If frame was not grabbed successfully, break the loop
    if not ret:
        print("Failed to grab frame")
        break

    # Perform inference on the frame
    results = model(frame)

    # Extract detections and draw bounding boxes on the frame
    for result in results:
        for box in result.boxes:
            # Get coordinates and draw bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the frame with the detections
    cv2.imshow('YOLOv8 Webcam', frame)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
