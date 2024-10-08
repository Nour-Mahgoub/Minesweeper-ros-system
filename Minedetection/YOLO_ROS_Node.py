
#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO

# Initialize YOLO model
model = YOLO('best.pt')  # Ensure 'best.pt' is the correct path to your YOLO model

class YoloRosNode:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('yolo_webcam_node', anonymous=True)

        # Create a CvBridge object to convert ROS images to OpenCV images
        self.bridge = CvBridge()

        # Subscribe to the topic (replace 'webcam_topic' with the actual topic name from Raspberry Pi)
        self.image_sub = rospy.Subscriber('/raspberry_pi/webcam', Image, self.image_callback)

        # Optional: To visualize the results
        self.visualize = True

    def image_callback(self, data):
        try:
            # Convert the ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

            # Perform YOLO inference on the image
            results = model(cv_image)

            # Extract detections and draw bounding boxes on the image
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Optionally display the result
            if self.visualize:
                cv2.imshow("YOLOv8 Detection", cv_image)
                cv2.waitKey(1)

        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))

if __name__ == '__main__':
    try:
        # Initialize and run the YOLO ROS node
        yolo_node = YoloRosNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()
