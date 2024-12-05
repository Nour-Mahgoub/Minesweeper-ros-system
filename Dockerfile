FROM ros:noetic-ros-base-focal

# Expose the Flask port
EXPOSE 5000

# Install Git and Python pip
RUN apt-get update && \
    apt-get install -y git python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install flask opencv-python