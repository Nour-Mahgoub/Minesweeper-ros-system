#include <ros/ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <sensor_msgs/Image.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>
#include "YOLO10.hpp"
#include <thread>
#include <atomic>
#include "tools/BoundedThreadSafeQueue.hpp"

class MineDetectionNode {
public:
    MineDetectionNode() : nh_("~"), detector_(nullptr) {
        // Load parameters
        std::string model_path, labels_path;
        nh_.param<std::string>("model_path", model_path, "../models/best.onnx");
        nh_.param<std::string>("labels_path", labels_path, "../models/coco.names");
        nh_.param<bool>("use_gpu", use_gpu_, true);
        
        // Initialize YOLO detector
        detector_ = new YOLO10Detector(model_path, labels_path, use_gpu_);
        
        // Set up publishers and subscribers
        camera_sub_ = nh_.subscribe("/camera_adapter_node/camera_feed", 1, &MineDetectionNode::cameraCallback, this);
        processed_pub_ = nh_.advertise<sensor_msgs::Image>("mine_feed_processed", 1);
        mine_detected_pub_ = nh_.advertise<std_msgs::Bool>("mine_detected", 1);
        
        // Initialize queues
        frameQueue = new BoundedThreadSafeQueue<cv::Mat>(2);
        processedQueue = new BoundedThreadSafeQueue<std::pair<cv::Mat, std::vector<Detection>>>(2);
        
        // Start processing threads
        stopFlag.store(false);
        consumer_thread_ = std::thread(&MineDetectionNode::consumerThread, this);
        display_thread_ = std::thread(&MineDetectionNode::displayThread, this);
    }
    
    ~MineDetectionNode() {
        stopFlag.store(true);
        frameQueue->set_finished();
        processedQueue->set_finished();
        consumer_thread_.join();
        display_thread_.join();
        delete detector_;
        delete frameQueue;
        delete processedQueue;
    }

private:
    ros::NodeHandle nh_;
    ros::Subscriber camera_sub_;
    ros::Publisher processed_pub_;
    ros::Publisher mine_detected_pub_;
    YOLO10Detector* detector_;
    bool use_gpu_;
    
    BoundedThreadSafeQueue<cv::Mat>* frameQueue;
    BoundedThreadSafeQueue<std::pair<cv::Mat, std::vector<Detection>>>* processedQueue;
    std::atomic<bool> stopFlag;
    std::thread consumer_thread_;
    std::thread display_thread_;

    void cameraCallback(const std_msgs::String::ConstPtr& msg) {
        // Decode base64 string to cv::Mat
        std::string decoded_str = base64_decode(msg->data);
        std::vector<uchar> data(decoded_str.begin(), decoded_str.end());
        cv::Mat frame = cv::imdecode(data, cv::IMREAD_COLOR);
        
        if (!frame.empty()) {
            frameQueue->enqueue(frame);
        }
    }

    void consumerThread() {
        cv::Mat frame;
        while (!stopFlag.load() && frameQueue->dequeue(frame)) {
            std::vector<Detection> detections = detector_->detect(frame);
            processedQueue->enqueue(std::make_pair(frame, detections));
        }
    }

    void displayThread() {
        std::pair<cv::Mat, std::vector<Detection>> item;
        while (!stopFlag.load() && processedQueue->dequeue(item)) {
            cv::Mat displayFrame = item.first;
            detector_->drawBoundingBoxMask(displayFrame, item.second);
            
            // Publish processed frame
            sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", displayFrame).toImageMsg();
            processed_pub_.publish(msg);
            
            // Publish mine detection status
            std_msgs::Bool mine_msg;
            mine_msg.data = !item.second.empty();  // True if any detections, false otherwise
            mine_detected_pub_.publish(mine_msg);
        }
    }

    std::string base64_decode(const std::string& encoded_string) {
        // Implement base64 decoding here
        // You can use a library like OpenSSL or implement it yourself
        // For brevity, I'm leaving this as a placeholder
        return encoded_string;  // This should be the decoded string
    }
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "mine_detection_node");
    MineDetectionNode node;
    ros::spin();
    return 0;
}