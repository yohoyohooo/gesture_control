#!/bin/bash

# Linux环境变量设置脚本
# 为手势识别无人机控制项目设置Linux环境变量

echo "设置Linux环境变量..."

# 设置Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 设置OpenCV后端 (避免GUI问题)
export OPENCV_VIDEOIO_PRIORITY_MSMF=0
export OPENCV_VIDEOIO_PRIORITY_V4L=1

# 设置GStreamer后端 (Linux首选)
export GST_VAAPI_ALL_DRIVERS=1

# 设置TensorFlow优化
export TF_CPP_MIN_LOG_LEVEL=2
export TF_ENABLE_ONEDNN_OPTS=1

# 设置PX4相关环境变量
export PX4_SIM_SPEED_FACTOR=1
export PX4_SIM_MODEL=iris

# 设置摄像头设备 (如果需要)
# export OPENCV_CAMERA_DEVICE=/dev/video0

# 设置MAVLink日志
export MAVLINK_VERBOSE=0

# 设置系统编码
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# 设置库路径 (如果需要)
# export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib"

echo "环境变量设置完成!"
echo "当前环境变量:"
echo "PYTHONPATH: $PYTHONPATH"
echo "LANG: $LANG"
echo "LC_ALL: $LC_ALL"

# 可选：显示系统信息
echo
echo "系统信息:"
echo "操作系统: $(uname -a)"
echo "Python路径: $(which python3)"
echo "Pip路径: $(which pip3)"

# 检查关键依赖
echo
echo "检查关键依赖:"
if python3 -c "import cv2; print('OpenCV: ✓')" 2>/dev/null; then
    echo "OpenCV: ✓"
else
    echo "OpenCV: ✗"
fi

if python3 -c "import tensorflow; print('TensorFlow: ✓')" 2>/dev/null; then
    echo "TensorFlow: ✓"
else
    echo "TensorFlow: ✗"
fi

if python3 -c "import mediapipe; print('MediaPipe: ✓')" 2>/dev/null; then
    echo "MediaPipe: ✓"
else
    echo "MediaPipe: ✗"
fi

echo
echo "提示: 运行 'source linux_env.sh' 来激活这些环境变量"
echo "或者将这些设置添加到你的 ~/.bashrc 文件中"
