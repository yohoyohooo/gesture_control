# 🚀 PX4无人机手势控制测试指南

本指南提供完整的测试流程，帮助你验证PX4无人机手势识别控制系统的所有功能。

## 📋 目录
1. [快速开始](#快速开始)
2. [环境检查](#环境检查)
3. [PX4仿真测试](#px4仿真测试)
4. [手势识别测试](#手势识别测试)
5. [集成测试](#集成测试)
6. [性能测试](#性能测试)
7. [故障排除](#故障排除)

## 快速开始

### 一键测试脚本

```bash
# 1. 启动PX4仿真 (Linux/Mac)
./start_px4_sitl.sh

# Windows
start_px4_sitl.bat

# 2. 在新终端测试连接
python tests/quick_px4_test.py

# 3. 运行主程序
python main.py
```

## 环境检查

### 检查依赖

```bash
# 检查Python版本
python3 --version

# 检查依赖包
python3 -c "
import sys
packages = ['cv2', 'numpy', 'tensorflow', 'mediapipe', 'pymavlink']
for pkg in packages:
    try:
        __import__(pkg.replace('cv2', 'cv2.cv2'))
        print(f'✓ {pkg}')
    except ImportError:
        print(f'✗ {pkg} - 需要安装')
"
```

### 检查硬件

```bash
# 检查摄像头
python3 -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('✓ 摄像头可用')
    ret, frame = cap.read()
    if ret:
        print(f'✓ 视频流正常 (分辨率: {frame.shape[1]}x{frame.shape[0]})')
    cap.release()
else:
    print('✗ 摄像头不可用')
"
```

## PX4仿真测试

### 启动仿真环境

```bash
# 方法1: 使用启动脚本
./start_px4_sitl.sh

# 方法2: 手动启动
cd ~/px4_ws/PX4-Autopilot
make px4_sitl gazebo
```

### 验证连接

```bash
# 快速连接测试
python tests/quick_px4_test.py

# 详细测试输出示例:
# ✓ pymavlink 导入成功
# 正在连接到PX4...
# ✓ 成功接收到心跳包!
#   系统ID: 1
#   组件ID: 1
#   系统类型: 2 (四旋翼)
#   飞行模式: STABILIZE
```

### 测试无人机类

```bash
# 测试PX4无人机类
python3 -c "
from drones.px4_drone import PX4Drone
drone = PX4Drone('udp:127.0.0.1:14550')
if drone.connect():
    print('✓ PX4连接成功')
    print(f'电池状态: {drone.get_battery()}')
    drone.end()
else:
    print('✗ PX4连接失败')
"
```

## 手势识别测试

### 测试手势识别模块

```bash
# 基本导入测试
python3 -c "
from gestures.gesture_recognition import GestureRecognition
print('✓ 手势识别模块导入成功')
"

# 摄像头测试
python3 -c "
import cv2
from gestures.gesture_recognition import GestureRecognition

cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        gesture_rec = GestureRecognition()
        debug_image, gesture_id = gesture_rec.recognize(frame)
        print(f'✓ 手势识别处理成功，检测到手势ID: {gesture_id}')
    cap.release()
else:
    print('✗ 摄像头不可用')
"
```

### 测试控制器

```bash
# 测试PX4手势控制器
python3 -c "
from gestures.px4_gesture_controller import PX4GestureController
from drones.px4_drone import PX4Drone

drone = PX4Drone('udp:127.0.0.1:14550')
controller = PX4GestureController(drone)
print('✓ PX4手势控制器创建成功')
"

# 测试键盘控制器
python3 -c "
from gestures.px4_keyboard_controller import PX4KeyboardController
from drones.px4_drone import PX4Drone

drone = PX4Drone('udp:127.0.0.1:14550')
controller = PX4KeyboardController(drone)
print('✓ PX4键盘控制器创建成功')
"
```

## 集成测试

### 完整系统测试

```bash
# 1. 启动PX4 SITL (终端1)
./start_px4_sitl.sh

# 2. 验证连接 (终端2)
python tests/quick_px4_test.py

# 3. 运行主程序 (终端2)
python main.py
```

### 测试流程

1. **启动程序**
   ```
   检测到无人机类型: PX4Drone
   PX4无人机支持手势和键盘控制模式
   ```

2. **起飞测试**
   - 按 `空格键` 起飞
   - 观察Gazebo中无人机是否起飞

3. **键盘控制测试**
   - 按 `k` 切换到键盘模式
   - 使用 `WASD` 移动，`QE` 旋转，`RF` 升降
   - 观察无人机响应

4. **手势控制测试**
   - 按 `g` 切换到手势模式
   - 对摄像头做出手势：
     - ✋ 停止
     - 👆 前进
     - 👈 上升
     - 👉 下降

## 性能测试

### FPS测试

```bash
python3 -c "
import cv2
import time
from gestures.gesture_recognition import GestureRecognition

cap = cv2.VideoCapture(0)
gesture_rec = GestureRecognition()

frame_count = 0
start_time = time.time()

while frame_count < 100:
    ret, frame = cap.read()
    if ret:
        debug_image, gesture_id = gesture_rec.recognize(frame)
        frame_count += 1

end_time = time.time()
fps = frame_count / (end_time - start_time)
print(f'平均FPS: {fps:.2f}')
cap.release()
"
```

### 延迟测试

```bash
# 测试手势到控制的延迟
python3 -c "
import time
from gestures.gesture_recognition import GestureRecognition, GestureBuffer

gesture_rec = GestureRecognition()
gesture_buffer = GestureBuffer(buffer_len=5)

# 模拟连续手势识别
start_time = time.time()
for i in range(50):
    # 这里需要实际的图像帧
    # debug_image, gesture_id = gesture_rec.recognize(frame)
    # gesture_buffer.add_gesture(gesture_id)
    pass

end_time = time.time()
avg_latency = (end_time - start_time) / 50 * 1000
print(f'平均延迟: {avg_latency:.2f}ms')
"
```

## 故障排除

### 常见问题

#### 1. PX4连接失败

```bash
# 检查PX4是否运行
ps aux | grep px4

# 检查端口
netstat -tulpn | grep 14550

# 重新启动PX4
./start_px4_sitl.sh
```

#### 2. 摄像头无法打开

```bash
# 检查摄像头设备
ls /dev/video*

# 测试OpenCV
python3 -c "import cv2; print(cv2.getBuildInformation())"
```

#### 3. 手势识别不准确

- 确保光照充足
- 手部在摄像头可视范围内 (30cm-1m)
- 避免背景复杂或光线不均
- 重新训练模型以适应你的手部特征

#### 4. 控制响应慢

- 检查MAVLink连接质量
- 减少视频分辨率
- 调整手势缓冲区大小 (config.txt中的buffer_len)

### 日志分析

```bash
# 启用详细日志
export MAVLINK_VERBOSE=1
python main.py 2>&1 | tee debug.log

# PX4日志
cd ~/px4_ws/PX4-Autopilot
tail -f build/px4_sitl_default/logs/*.ulg
```

### 性能调优

```txt
# config.txt 优化配置
device = 0
width = 640          # 降低分辨率
height = 480
buffer_len = 3       # 减少缓冲区
px4_connection_string = udp:127.0.0.1:14550
```

## 📊 测试报告模板

```
测试日期: YYYY-MM-DD
测试环境: [Ubuntu 20.04 / Windows WSL / macOS]
硬件配置: [CPU, RAM, GPU]

测试项目:
□ PX4 SITL启动
□ MAVLink连接
□ 手势识别
□ 键盘控制
□ 手势控制
□ 完整集成测试

性能指标:
- 手势识别FPS: ____
- 控制延迟: ____ ms
- CPU使用率: ____ %
- 内存使用: ____ MB

问题记录:
1. ____________________
2. ____________________

结论: [通过/需要改进/失败]
```

---

🎯 **测试完成标准**

- [ ] PX4 SITL成功启动并连接
- [ ] 手势识别准确率 > 90%
- [ ] 控制响应延迟 < 200ms
- [ ] 支持键盘和手势两种控制模式
- [ ] 系统稳定运行 > 10分钟

按照此指南逐步测试，你就能全面验证PX4无人机手势控制系统的功能和性能！
