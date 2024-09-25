# Minesweeper ROS Backend

## Description
- ROS backend for the minesweeper robot developed by Zewail City Aquila 23 SC team.

## How to Run
### Automatically
```
1- configure your network then write its IPs in the settings.json and docker-compose.yml files
2- python ros_launch.py
```
### MANUALLY
```
1- configure your network then write its IPs in the settings.json and docker-compose.yml files (for the docker.compose.yml add the main cu IP in both the main cu and raspi)
2- run the following command to initialize the ros master `docker compose up -d` or `sudo docker compose up -d` in main cu and raspi
3- Initialize your needed nodes by running the bootstrap file of it from the main directory like the following for example only: `python ros_nodes/camera_adapter_node/bootstrap.py`
``` 

## Required Dependencies
```
python3.10+
docker
rospy
pygame
```

## Provided Libraries
- settings.py: parses the settings.json file into a python runtime object
- serial_driver.py: provides reliable serial communication API
- log.py: logging manager for easier debugging
- ros.py: helps integrating your node with the entire ROS backend
- Aruco_Modular.py: for Aruco Detection and calibration -- `needs opencv-contrib to run`
- BaslerCameraModule.py: Module facilitates communication with a Basler camera
- mapping.py: custom mapping algorithms using trilateration concept of mapping