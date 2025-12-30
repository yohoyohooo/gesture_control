# 🐧 Linux部署指南

本项目已针对Linux系统进行了优化和适配。本文档提供在Linux系统上部署和运行的完整指南。

## 📋 目录
1. [快速开始](#快速开始)
2. [系统要求](#系统要求)
3. [一键部署](#一键部署)
4. [手动安装](#手动安装)
5. [环境配置](#环境配置)
6. [运行测试](#运行测试)
7. [故障排除](#故障排除)
8. [性能优化](#性能优化)

## 快速开始

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd gesture-control

# 2. 运行兼容性检查
./linux_compatibility_check.sh

# 3. 一键部署
./linux_deploy.sh

# 4. 设置环境变量
source linux_env.sh

# 5. 运行程序
python3 main.py
```

## 系统要求

### 推荐配置
- **操作系统**: Ubuntu 18.04/20.04/22.04 LTS
- **CPU**: Intel i5 或 AMD Ryzen 5 (或更高)
- **内存**: 8GB RAM (推荐16GB)
- **存储**: 20GB可用空间
- **显卡**: NVIDIA GTX 1050 或更高 (可选，用于GPU加速)

### 支持的发行版
- ✅ Ubuntu/Debian
- ✅ Fedora/CentOS/RHEL
- ✅ Arch Linux/Manjaro
- ✅ openSUSE

## 一键部署

运行自动部署脚本：

```bash
./linux_deploy.sh
```

该脚本将自动：
- ✅ 更新系统包
- ✅ 安装系统依赖 (OpenCV, GStreamer等)
- ✅ 安装Python依赖包
- ✅ 配置摄像头权限
- ✅ 设置脚本执行权限
- ✅ 创建桌面启动器
- ✅ 验证安装完整性

### 部署选项

脚本会询问是否安装可选组件：

1. **PX4 SITL仿真环境** (推荐)
   - 安装PX4开发环境
   - 配置Gazebo仿真器
   - 设置MAVLink通信

2. **桌面启动器**
   - 创建应用程序菜单项
   - 支持双击启动

## 手动安装

如果自动部署失败，可以手动安装：

### 1. 系统依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y \
    python3 python3-pip python3-dev \
    git curl wget \
    build-essential cmake ninja-build \
    libgtk-3-dev libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libjpeg-dev libpng-dev libtiff-dev \
    libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev \
    libatlas-base-dev gfortran \
    libhdf5-dev libhdf5-serial-dev

# Fedora/CentOS
sudo dnf install -y \
    python3 python3-pip python3-devel \
    git cmake ninja-build \
    gtk3-devel gstreamer1-devel \
    gstreamer1-plugins-base-devel \
    libjpeg-turbo-devel libpng-devel libtiff-devel \
    ffmpeg-devel libv4l-devel \
    atlas-devel lapack-devel \
    hdf5-devel

# Arch Linux
sudo pacman -S \
    python python-pip \
    git cmake ninja \
    gtk3 gstreamer gst-plugins-base \
    ffmpeg libv4l \
    lapack hdf5
```

### 2. Python依赖

```bash
# 升级pip
pip3 install --upgrade pip

# 安装项目依赖
pip3 install -r requirements.txt

# 或者手动安装核心包
pip3 install \
    opencv-python \
    numpy \
    tensorflow \
    mediapipe \
    pymavlink \
    ConfigArgParse \
    djitellopy
```

### 3. 摄像头权限配置

```bash
# 将当前用户添加到video组
sudo usermod -a -G video $USER

# 重新登录或运行以下命令使权限生效
newgrp video

# 验证权限
groups $USER
ls -la /dev/video0
```

## 环境配置

### 环境变量

运行环境配置脚本：

```bash
source linux_env.sh
```

该脚本设置：
- ✅ Python路径
- ✅ OpenCV后端配置
- ✅ TensorFlow优化
- ✅ PX4仿真参数
- ✅ 系统编码

### 配置文件

复制Linux配置文件：

```bash
cp config.linux.txt config.txt
```

编辑配置文件以适应你的系统：

```txt
# 摄像头设备 (如果需要指定)
camera_device = /dev/video0

# PX4日志目录
px4_log_dir = ~/px4_ws/PX4-Autopilot/build/px4_sitl_default/logs

# 视频分辨率 (根据硬件性能调整)
width = 640
height = 480
```

## 运行测试

### 1. 兼容性测试

```bash
./linux_compatibility_check.sh
```

### 2. 模块测试

```bash
# 测试核心模块
python3 -c "
from drones.drone_detector import DroneDetector
from gestures.gesture_recognition import GestureRecognition
from gestures.px4_gesture_controller import PX4GestureController
print('✅ 所有核心模块正常')
"
```

### 3. 摄像头测试

```bash
# 测试摄像头
python3 -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print(f'✅ 摄像头正常: {frame.shape}')
    cap.release()
else:
    print('❌ 摄像头不可用')
"
```

### 4. PX4连接测试

```bash
# 启动PX4 SITL
./start_px4_sitl.sh

# 在新终端测试连接
python3 tests/quick_px4_test.py
```

### 5. 完整系统测试

```bash
python3 main.py
```

## 故障排除

### 常见问题

#### 1. OpenCV安装失败

**问题**: `ImportError: libGL.so.1`

**解决**:
```bash
# 安装OpenGL库
sudo apt install -y libgl1-mesa-glx libglib2.0-0

# 或者使用headless版本
pip3 uninstall opencv-python
pip3 install opencv-python-headless
```

#### 2. TensorFlow性能问题

**问题**: TensorFlow运行慢

**解决**:
```bash
# 安装GPU版本 (如果有NVIDIA GPU)
pip3 install tensorflow-gpu

# 或者使用CPU优化版本
pip3 install tensorflow-cpu
```

#### 3. 摄像头权限问题

**问题**: `Permission denied: /dev/video0`

**解决**:
```bash
# 检查用户组
groups $USER

# 添加到video组
sudo usermod -a -G video $USER
newgrp video

# 如果仍然失败，检查设备权限
ls -la /dev/video0
sudo chmod 666 /dev/video0
```

#### 4. GStreamer错误

**问题**: GStreamer插件缺失

**解决**:
```bash
sudo apt install -y \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav
```

#### 5. PX4连接失败

**问题**: 无法连接到PX4

**检查**:
```bash
# 检查PX4是否运行
ps aux | grep px4

# 检查端口
netstat -tuln | grep 14550

# 检查防火墙
sudo ufw status
```

### 调试模式

启用详细日志：

```bash
# 运行时显示详细日志
export MAVLINK_VERBOSE=1
export TF_CPP_MIN_LOG_LEVEL=0
python3 main.py 2>&1 | tee debug.log
```

### 系统信息收集

```bash
# 收集系统信息用于诊断
./linux_compatibility_check.sh > system_info.log
```

## 性能优化

### CPU优化

```bash
# 使用多线程
export OMP_NUM_THREADS=$(nproc)
export MKL_NUM_THREADS=$(nproc)

# TensorFlow优化
export TF_CPP_MIN_LOG_LEVEL=2
export TF_ENABLE_ONEDNN_OPTS=1
```

### GPU优化 (NVIDIA)

```bash
# 安装CUDA和cuDNN
# 然后安装GPU版本TensorFlow
pip3 install tensorflow-gpu

# 设置GPU内存增长
export TF_FORCE_GPU_ALLOW_GROWTH=true
```

### 视频优化

```txt
# config.txt - 降低分辨率以提高性能
width = 640
height = 480
min_detection_confidence = 0.5
min_tracking_confidence = 0.5
```

### 系统优化

```bash
# 增加文件描述符限制
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# 禁用swap (如果内存充足)
sudo swapoff -a
```

## 生产环境部署

### Systemd服务

创建系统服务：

```bash
# 创建服务文件
sudo tee /etc/systemd/system/drone-gesture-control.service > /dev/null <<EOF
[Unit]
Description=Drone Gesture Control Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(which python3) main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 启用和启动服务
sudo systemctl enable drone-gesture-control
sudo systemctl start drone-gesture-control

# 查看状态
sudo systemctl status drone-gesture-control
```

### Docker部署

```dockerfile
FROM ubuntu:20.04

# 安装系统依赖
RUN apt update && apt install -y \
    python3 python3-pip \
    libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip3 install -r requirements.txt

# 创建非root用户
RUN useradd -m drone && chown -R drone:drone /app
USER drone

# 启动命令
CMD ["python3", "main.py"]
```

构建和运行：

```bash
# 构建镜像
docker build -t drone-gesture-control .

# 运行容器 (需要摄像头访问)
docker run -it --device=/dev/video0 --network=host drone-gesture-control
```

## 📚 参考资料

- [Ubuntu OpenCV安装指南](https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html)
- [TensorFlow GPU指南](https://www.tensorflow.org/install/gpu)
- [PX4 Linux设置](https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html)
- [MediaPipe Linux要求](https://developers.google.com/mediapipe/getting_started/python)

---

🎉 **恭喜！** 现在你可以在Linux系统上完美运行手势识别无人机控制系统了！

有任何Linux相关的问题都可以参考此文档或运行 `./linux_compatibility_check.sh` 进行诊断。
