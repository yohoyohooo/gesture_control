#!/bin/bash

# PX4 SITL一键启动脚本
# 用于快速启动PX4仿真环境进行测试

echo "======================================="
echo "    PX4 SITL 启动脚本"
echo "======================================="

# 检查PX4工作目录
PX4_DIR="$HOME/px4_ws/PX4-Autopilot"
if [ ! -d "$PX4_DIR" ]; then
    echo "错误: PX4目录不存在: $PX4_DIR"
    echo "请先按照 PX4_SITL_SETUP.md 安装PX4"
    exit 1
fi

cd "$PX4_DIR"

echo "进入PX4目录: $PWD"

# 检查是否已经运行
if pgrep -f "px4" > /dev/null; then
    echo "警告: 发现PX4进程正在运行"
    read -p "是否要停止现有进程并重新启动? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -f px4
        sleep 2
    else
        echo "退出启动脚本"
        exit 0
    fi
fi

# 选择仿真器
echo "选择仿真器:"
echo "1) Gazebo (推荐，有GUI)"
echo "2) jmavsim (轻量，无GUI)"
read -p "请输入选择 (1或2): " -n 1 -r
echo

case $REPLY in
    1)
        SIMULATOR="gazebo"
        ;;
    2)
        SIMULATOR="jmavsim"
        ;;
    *)
        echo "无效选择，使用Gazebo"
        SIMULATOR="gazebo"
        ;;
esac

# 选择机架类型
echo "选择机架类型:"
echo "1) 四旋翼 (iris) - 默认"
echo "2) 固定翼 (plane)"
echo "3)  rover (地面车辆)"
read -p "请输入选择 (1-3): " -n 1 -r
echo

case $REPLY in
    1)
        VEHICLE=""
        ;;
    2)
        VEHICLE="_plane"
        ;;
    3)
        VEHICLE="_rover"
        ;;
    *)
        VEHICLE=""
        ;;
esac

# 构建命令
COMMAND="make px4_sitl ${SIMULATOR}${VEHICLE}"

echo "启动命令: $COMMAND"
echo "======================================="

# 执行命令
eval $COMMAND

echo "======================================="
echo "PX4 SITL 已停止"
