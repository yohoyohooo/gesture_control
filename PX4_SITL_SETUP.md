# PX4 SITL仿真环境设置指南

本指南将帮助你在本地计算机上设置PX4 SITL（Software In The Loop）仿真环境，用于测试手势识别无人机控制代码。

## 📋 目录
1. [环境要求](#环境要求)
2. [安装PX4开发环境](#安装px4开发环境)
3. [下载和编译PX4固件](#下载和编译px4固件)
4. [启动SITL仿真](#启动sitl仿真)
5. [配置MAVLink连接](#配置mavlink连接)
6. [测试无人机控制](#测试无人机控制)
7. [集成手势识别](#集成手势识别)
8. [故障排除](#故障排除)

## 环境要求

### 系统要求
- **操作系统**: Ubuntu 18.04/20.04 (推荐) 或 macOS/Windows (WSL)
- **内存**: 至少8GB RAM
- **存储**: 至少20GB可用空间
- **网络**: 稳定的互联网连接

### 依赖软件
- Git
- Python 3.6+
- CMake
- Ninja
- GCC/G++编译器

## 安装PX4开发环境

### Ubuntu/Debian (推荐)

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础依赖
sudo apt install -y \
    git \
    python3 \
    python3-pip \
    cmake \
    ninja-build \
    g++ \
    gcc \
    make \
    unzip \
    wget \
    curl

# 安装Python依赖
pip3 install --user kconfiglib jsonschema jinja2

# 可选：安装Gazebo仿真器 (用于可视化)
sudo apt install -y \
    gazebo9 \
    libgazebo9-dev \
    gazebo9-plugin-base \
    libgazebo9-dev \
    libjansson-dev \
    libignition-math4-dev \
    libsdformat6-dev
```

### macOS

```bash
# 使用Homebrew安装依赖
brew install git python3 cmake ninja gcc make

# 安装Python依赖
pip3 install --user kconfiglib jsonschema jinja2
```

### Windows (WSL)

推荐使用Windows Subsystem for Linux (WSL2) + Ubuntu，然后按照Ubuntu步骤安装。

## 下载和编译PX4固件

```bash
# 创建工作目录
mkdir -p ~/px4_ws && cd ~/px4_ws

# 克隆PX4源码 (主分支)
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot

# 如果网络慢，可以使用国内镜像
# git clone https://gitee.com/PX4/PX4-Autopilot.git --recursive

# 初始化子模块
git submodule update --init --recursive

# 配置环境
bash ./Tools/setup/ubuntu.sh

# 重新启动终端或运行
source ~/.bashrc

# 编译SITL仿真版本
make px4_sitl_default
```

编译可能需要10-30分钟，取决于你的计算机性能。

## 启动SITL仿真

### 基本启动

```bash
cd ~/px4_ws/PX4-Autopilot

# 启动SITL仿真 (使用Gazebo)
make px4_sitl gazebo

# 或者只启动PX4 SITL (无GUI)
make px4_sitl jmavsim
```

### 常用启动参数

```bash
# 指定UDP端口
make px4_sitl gazebo UDP_PORT=14550

# 指定串口设备 (如果连接真实硬件)
make px4_sitl gazebo /dev/ttyACM0

# 使用特定的机架配置
make px4_sitl gazebo_iris  # 四旋翼
make px4_sitl gazebo_plane  # 固定翼
```

### 后台运行

```bash
# 后台启动
make px4_sitl gazebo &
```

## 配置MAVLink连接

SITL启动后，会自动在UDP端口14550上监听MAVLink连接。

### 检查连接

```bash
# 安装MAVLink工具 (如果还没有)
pip3 install pymavlink

# 测试连接
python3 -c "
from pymavlink import mavutil
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()
print('连接成功!')
print(f'系统ID: {master.target_system}')
print(f'组件ID: {master.target_component}')
"
```

### 修改项目配置

在你的手势识别项目中，确保 `config.txt` 中的连接字符串正确：

```txt
px4_connection_string = udp:127.0.0.1:14550
```

## 测试无人机控制

### 1. 启动SITL

```bash
cd ~/px4_ws/PX4-Autopilot
make px4_sitl gazebo
```

### 2. 在新终端中运行你的程序

```bash
cd /path/to/your/gesture-control
python main.py
```

### 3. 预期的行为

程序会：
1. 首先尝试连接Tello（失败）
2. 然后连接PX4 SITL（成功）
3. 显示"PX4无人机支持手势和键盘控制模式"
4. 等待你按空格键起飞

### 4. 控制测试

- **起飞**: 按空格键
- **键盘控制**: 按 'k' 切换到键盘模式，然后用 WASD 控制
- **手势控制**: 按 'g' 切换到手势模式（需要摄像头）

## 集成手势识别

### 硬件要求

- USB摄像头或内置摄像头
- 足够的光照
- 手势识别距离：30cm-1m

### 测试步骤

1. **启动PX4 SITL**
   ```bash
   make px4_sitl gazebo
   ```

2. **运行手势控制程序**
   ```bash
   python main.py
   ```

3. **起飞并切换模式**
   - 按空格键起飞
   - 按 'g' 进入手势控制模式

4. **测试手势**
   - ✋ **手掌** - 停止
   - 👆 **食指** - 前进
   - 👈 **握拳** - 上升
   - 👉 **OK手势** - 下降
   - 🤏 **捏手** - 左转
   - 🖖 **V手势** - 右转

## 故障排除

### 常见问题

#### 1. SITL启动失败

**问题**: `make px4_sitl gazebo` 失败

**解决方案**:
```bash
# 清理并重新编译
make clean
make px4_sitl_default

# 检查依赖
sudo apt install -y libgstreamer-plugins-base1.0-dev
```

#### 2. 连接失败

**问题**: 程序显示"未识别到支持的无人机类型"

**检查**:
```bash
# 确认SITL正在运行
netstat -tulpn | grep 14550

# 测试MAVLink连接
python3 -c "from pymavlink import mavutil; mavutil.mavlink_connection('udp:127.0.0.1:14550').wait_heartbeat(timeout=5)"
```

#### 3. Gazebo无法启动

**问题**: GUI无法显示

**解决方案**:
```bash
# 使用无GUI模式
make px4_sitl jmavsim

# 或者检查显示设置
export DISPLAY=:0
```

#### 4. 手势识别不工作

**检查**:
- 摄像头是否正确连接
- OpenCV是否安装：`python3 -c "import cv2; print('OpenCV OK')"`
- 光照是否充足
- 手势是否在识别范围内

### 日志调试

```bash
# PX4日志
cd ~/px4_ws/PX4-Autopilot
tail -f build/px4_sitl_default/logs/*.ulg

# Python程序日志
python main.py 2>&1 | tee debug.log
```

### 性能优化

```bash
# 减少SITL负载
export PX4_SIM_SPEED_FACTOR=1

# 调整视频分辨率 (在config.txt中)
width = 640
height = 480
```

## 高级配置

### 自定义参数

```bash
# 修改PX4参数
cd ~/px4_ws/PX4-Autopilot
make px4_sitl gazebo UPLOAD_PARAMS=1 PARAM_FILE=/path/to/params.txt
```

### 多机仿真

```bash
# 启动多个SITL实例
make px4_sitl gazebo UDP_PORT=14550 &
make px4_sitl gazebo UDP_PORT=14560 &
```

### 与真实硬件混合测试

```bash
# SITL + 真实硬件
make px4_sitl gazebo UDP_PORT=14550 SERIAL_DEVICE=/dev/ttyACM0
```

## 📚 参考资料

- [PX4官方文档](https://docs.px4.io/)
- [PX4开发者指南](https://dev.px4.io/)
- [MAVLink协议文档](https://mavlink.io/)
- [Gazebo仿真教程](https://gazebosim.org/tutorials)

---

🎉 **恭喜！** 现在你有了一个完整的PX4仿真测试环境，可以开始测试你的手势识别无人机控制系统了！

有任何问题都可以查看故障排除部分或查阅官方文档。
