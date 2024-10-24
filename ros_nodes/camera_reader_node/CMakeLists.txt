cmake_minimum_required(VERSION 3.0.0)
project(yolo_ort)

option(ONNXRUNTIME_DIR "Path to built ONNX Runtime directory." STRING)
message(STATUS "ONNXRUNTIME_DIR: ${ONNXRUNTIME_DIR}")

find_package(OpenCV REQUIRED)

include_directories("include/")

# Add executable for image inference
add_executable(image_inference src/image_inference.cpp)

# Add executable for camera inference
add_executable(camera_inference src/camera_inference.cpp)

# Add executable for video inference
add_executable(video_inference src/video_inference.cpp)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set include directories for all executables (better to use target_include_directories)
target_include_directories(image_inference PRIVATE "${ONNXRUNTIME_DIR}/include")
target_include_directories(camera_inference PRIVATE "${ONNXRUNTIME_DIR}/include")
target_include_directories(video_inference PRIVATE "${ONNXRUNTIME_DIR}/include")


# Link libraries for all executables  **<-- KEY CHANGES HERE**
target_link_libraries(image_inference ${OpenCV_LIBS} pthread)
if(WIN32)
    target_link_libraries(image_inference "${ONNXRUNTIME_DIR}/lib/onnxruntime.lib")
elseif(UNIX)
    target_link_libraries(image_inference "${ONNXRUNTIME_DIR}/lib/libonnxruntime.so")
endif()

target_link_libraries(camera_inference ${OpenCV_LIBS} pthread)
if(WIN32)
    target_link_libraries(camera_inference "${ONNXRUNTIME_DIR}/lib/onnxruntime.lib")
elseif(UNIX)
    target_link_libraries(camera_inference "${ONNXRUNTIME_DIR}/lib/libonnxruntime.so")
endif()

target_link_libraries(video_inference ${OpenCV_LIBS} pthread)
if(WIN32)
  target_link_libraries(video_inference "${ONNXRUNTIME_DIR}/lib/onnxruntime.lib")
elseif(UNIX)
  target_link_libraries(video_inference "${ONNXRUNTIME_DIR}/lib/libonnxruntime.so")
endif()



# Removed redundant compile features setting (CXX_STANDARD already handles this)
