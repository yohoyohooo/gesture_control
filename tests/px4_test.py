#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PX4无人机测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_px4_imports():
    """测试PX4相关模块导入"""
    try:
        from drones.px4_drone import PX4Drone
        print("[OK] PX4Drone 导入成功")
    except ImportError as e:
        print(f"[FAIL] PX4Drone 导入失败: {e}")

    try:
        from gestures.px4_gesture_controller import PX4GestureController
        print("[OK] PX4GestureController 导入成功")
    except ImportError as e:
        print(f"[FAIL] PX4GestureController 导入失败: {e}")

def test_px4_instantiation():
    """测试PX4实例化"""
    try:
        from drones.px4_drone import PX4Drone
        px4 = PX4Drone("udp:127.0.0.1:14550")
        print("[OK] PX4Drone 实例化成功")
        print(f"  - 连接字符串: {px4.connection_string}")
        print(f"  - 已连接: {px4.connected}")
    except Exception as e:
        print(f"[FAIL] PX4Drone 实例化失败: {e}")

def test_px4_controller_instantiation():
    """测试PX4控制器实例化"""
    try:
        from drones.px4_drone import PX4Drone
        from gestures.px4_gesture_controller import PX4GestureController

        px4 = PX4Drone("udp:127.0.0.1:14550")
        controller = PX4GestureController(px4)
        print("[OK] PX4GestureController 实例化成功")
        print(f"  - 最大速度: {controller.max_velocity}")
    except Exception as e:
        print(f"[FAIL] PX4GestureController 实例化失败: {e}")

if __name__ == "__main__":
    print("开始PX4功能测试...")
    print("=" * 50)

    test_px4_imports()
    print()

    test_px4_instantiation()
    print()

    test_px4_controller_instantiation()
    print()

    print("=" * 50)
    print("PX4功能测试完成")
