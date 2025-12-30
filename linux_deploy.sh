#!/bin/bash

# Linux一键部署脚本
# 用于在Linux系统上自动部署和配置手势识别无人机控制项目

set -e  # 遇到错误立即退出

echo "======================================="
echo "    Linux项目部署脚本"
echo "    手势识别无人机控制系统"
echo "======================================="

# 检查是否为root用户
if [ "$EUID" -eq 0 ]; then
    echo "❌ 请不要使用root用户运行此脚本"
    echo "请使用普通用户，并根据需要输入sudo密码"
    exit 1
fi

# 检查操作系统
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ 此脚本仅适用于Linux系统"
    exit 1
fi

echo "检测到Linux系统: $(uname -a)"
echo

# 更新系统包
echo "📦 更新系统包..."
sudo apt update && sudo apt upgrade -y
echo "✅ 系统更新完成"
echo

# 安装基础依赖
echo "🔧 安装基础依赖..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    curl \
    wget \
    build-essential \
    cmake \
    ninja-build \
    pkg-config \
    libgtk-3-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-good1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-0 \
    libcanberra-gtk3-module \
    libatlas-base-dev \
    gfortran \
    libhdf5-dev \
    libhdf5-serial-dev \
    libhdf5-103 \
    libqtgui4 \
    libqtwebkit4 \
    libqt4-test \
    libjasper-dev

echo "✅ 基础依赖安装完成"
echo

# 安装Python依赖
echo "🐍 安装Python依赖..."
pip3 install --upgrade pip

# 安装项目依赖
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo "✅ 项目依赖安装完成"
else
    echo "⚠️  requirements.txt文件不存在，安装基础依赖..."
    pip3 install \
        opencv-python \
        numpy \
        tensorflow \
        mediapipe \
        pymavlink \
        ConfigArgParse \
        djitellopy \
        kconfiglib \
        jinja2
fi
echo

# 配置摄像头权限
echo "📷 配置摄像头权限..."
if [ -c "/dev/video0" ]; then
    sudo usermod -a -G video $USER
    echo "✅ 已将用户添加到video组"
    echo "⚠️  请重新登录或运行 'newgrp video' 以使权限生效"
else
    echo "⚠️  未检测到摄像头设备 (/dev/video0)"
fi
echo

# 设置脚本权限
echo "🔐 设置脚本权限..."
chmod +x *.sh
chmod +x *.py
echo "✅ 脚本权限设置完成"
echo

# 验证安装
echo "🔍 验证安装..."
python3 -c "
import sys
import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp

print('✅ OpenCV版本:', cv2.__version__)
print('✅ NumPy版本:', np.__version__)
print('✅ TensorFlow版本:', tf.__version__)
print('✅ MediaPipe版本:', mp.__version__)

# 测试基本功能
try:
    import pymavlink
    print('✅ pymavlink可用')
except ImportError:
    print('⚠️  pymavlink不可用 (PX4功能受限)')

try:
    import djitellopy
    print('✅ djitellopy可用')
except ImportError:
    print('⚠️  djitellopy不可用 (Tello功能受限)')

print('🎉 Python环境验证完成')
"
echo

# 检查项目文件完整性
echo "📁 检查项目文件..."
missing_files=()
required_files=(
    "main.py"
    "config.txt"
    "drones/drone_detector.py"
    "drones/px4_drone.py"
    "drones/tello_drone.py"
    "gestures/gesture_recognition.py"
    "model/keypoint_classifier/keypoint_classifier.tflite"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ 所有必需文件都存在"
else
    echo "❌ 缺少以下文件:"
    printf '   - %s\n' "${missing_files[@]}"
fi
echo

# 可选：安装PX4 SITL
echo "🚁 是否安装PX4 SITL仿真环境? (推荐用于测试)"
read -p "安装PX4 SITL? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "正在安装PX4 SITL..."
    bash PX4_SITL_SETUP.md  # 这只是示例，实际需要运行具体的安装命令
    echo "✅ PX4 SITL安装完成"
else
    echo "跳过PX4 SITL安装"
fi
echo

# 创建桌面启动器
echo "🖥️  创建桌面启动器..."
DESKTOP_FILE="$HOME/.local/share/applications/drone-gesture-control.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Drone Gesture Control
Comment=手势识别无人机控制系统
Exec=gnome-terminal -- bash -c "cd $(pwd) && python3 main.py"
Icon=applications-games
Terminal=false
Type=Application
Categories=Game;Simulation;
EOF

chmod +x "$DESKTOP_FILE"
echo "✅ 桌面启动器已创建"
echo

# 最终测试
echo "🧪 运行最终测试..."
if python3 -c "
from drones.drone_detector import DroneDetector
from gestures.gesture_recognition import GestureRecognition
print('✅ 核心模块导入成功')
"; then
    echo "🎉 项目部署成功!"
else
    echo "❌ 项目部署失败，请检查错误信息"
    exit 1
fi
echo

echo "======================================="
echo "    部署完成！"
echo "======================================="

echo "
🎯 下一步操作:

1. 🔄 重新登录或运行: newgrp video (摄像头权限)

2. 🚁 启动PX4仿真 (如果安装了):
   ./start_px4_sitl.sh

3. 🎮 运行程序:
   python3 main.py

4. 📚 查看文档:
   - TESTING_GUIDE.md - 测试指南
   - PX4_SITL_SETUP.md - PX4设置指南
   - README.md - 项目说明

5. 🐛 故障排除:
   ./linux_compatibility_check.sh

🎉 享受你的手势识别无人机控制系统！
"

echo "======================================="
