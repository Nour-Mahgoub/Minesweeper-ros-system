import os
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('best.pt')  # Replace 'best.pt' with the path to your model if needed

# Define the input and output folders
input_folder = 'test/images'  # Replace with the actual path to your test images folder
output_folder = 'Output'  # Replace with the actual path for saving output images

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through the test images and perform inference
for image_name in os.listdir(input_folder):
    # Check if the file is an image
    if image_name.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
        # Read the image
        image_path = os.path.join(input_folder, image_name)
        image = cv2.imread(image_path)

        # Perform inference
        results = model(image)

        # Extract detections
        for result in results:
            # Draw bounding boxes on the image
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                confidence = box.conf[0]  # Confidence score
                class_id = int(box.cls[0])  # Class id (should be 'mine' as the only class)

                # Draw rectangle and label on the image
                label = f"mine {confidence:.2f}"
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Save the image with detected objects in the output folder
        output_path = os.path.join(output_folder, image_name)
        cv2.imwrite(output_path, image)

print("Inference completed and images saved to:", output_folder)
