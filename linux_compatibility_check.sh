#!/bin/bash

# Linux兼容性检查脚本
# 检查项目在Linux环境下的兼容性问题

echo "======================================="
echo "    Linux兼容性检查"
echo "======================================="

# 检查操作系统
echo "操作系统信息:"
uname -a
echo

# 检查Python版本
echo "Python版本:"
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3未安装"
    exit 1
fi
echo

# 检查pip
echo "Pip版本:"
pip3 --version
if [ $? -ne 0 ]; then
    echo "❌ pip3未安装"
    exit 1
fi
echo

# 检查依赖包
echo "检查Python依赖包..."
python3 -c "
import sys
required_packages = [
    'cv2', 'numpy', 'tensorflow', 'mediapipe',
    'pymavlink', 'configargparse', 'djitellopy'
]

missing_packages = []
for package in required_packages:
    try:
        if package == 'cv2':
            import cv2
        else:
            __import__(package)
        print(f'✅ {package}')
    except ImportError:
        print(f'❌ {package} - 需要安装')
        missing_packages.append(package)

if missing_packages:
    print()
    print('安装缺失的包:')
    echo 'pip3 install ' + ' '.join(missing_packages)
else:
    print('所有Python依赖包已安装')
"
echo

# 检查文件权限
echo "检查脚本权限..."
scripts=(
    "main.py"
    "start_px4_sitl.sh"
    "linux_compatibility_check.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo "✅ $script - 可执行"
        else
            echo "⚠️  $script - 不可执行，正在修复..."
            chmod +x "$script"
            echo "✅ $script - 权限已修复"
        fi
    else
        echo "⚠️  $script - 文件不存在"
    fi
done
echo

# 检查目录结构
echo "检查项目目录结构..."
required_dirs=(
    "drones"
    "gestures"
    "model"
    "tests"
    "utils"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ - 目录存在"
    else
        echo "❌ $dir/ - 目录不存在"
    fi
done
echo

# 检查关键文件
echo "检查关键文件..."
key_files=(
    "config.txt"
    "requirements.txt"
    "model/keypoint_classifier/keypoint_classifier.tflite"
    "model/point_history_classifier/point_history_classifier.tflite"
)

for file in "${key_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file - 文件存在"
    else
        echo "❌ $file - 文件不存在"
    fi
done
echo

# 检查摄像头访问权限
echo "检查摄像头访问权限..."
if [ -c "/dev/video0" ]; then
    echo "✅ /dev/video0 - 摄像头设备存在"
    # 检查当前用户是否有访问权限
    if groups $USER | grep -q "video"; then
        echo "✅ 用户在video组中"
    else
        echo "⚠️  用户不在video组中，可能无法访问摄像头"
        echo "   解决方法: sudo usermod -a -G video $USER"
    fi
else
    echo "⚠️  /dev/video0 - 摄像头设备不存在"
fi
echo

# 检查网络端口
echo "检查网络端口可用性..."
if command -v netstat &> /dev/null; then
    if netstat -tuln | grep -q ":14550 "; then
        echo "⚠️  端口14550已被占用 (PX4默认端口)"
    else
        echo "✅ 端口14550可用"
    fi
else
    echo "⚠️  netstat命令不可用，跳过端口检查"
fi
echo

echo "======================================="
echo "    兼容性检查完成"
echo "======================================="

echo "
📋 总结和建议:

1. 🔧 安装依赖:
   pip3 install -r requirements.txt

2. 📷 摄像头权限 (如果需要):
   sudo usermod -a -G video \$USER
   # 重新登录或运行: newgrp video

3. 🚁 PX4仿真 (可选):
   按照 PX4_SITL_SETUP.md 安装PX4 SITL

4. 🧪 测试运行:
   python3 main.py

5. 🔍 故障排除:
   查看 TESTING_GUIDE.md 获取详细测试指南
"

echo "======================================="
