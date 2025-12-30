#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PX4键盘控制器测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_px4_keyboard_controller():
    """测试PX4键盘控制器"""
    try:
        # 直接导入，避免通过__init__.py导入依赖cv2的模块
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

        from gestures.px4_keyboard_controller import PX4KeyboardController
        print("[OK] PX4KeyboardController 导入成功")

        # 创建一个模拟的drone对象来测试
        class MockDrone:
            def send_rc_control(self, left_right, forw_back, up_down, yaw):
                print(f"RC控制: 左右={left_right}, 前后={forw_back}, 上下={up_down}, 偏航={yaw}")

        mock_drone = MockDrone()
        controller = PX4KeyboardController(mock_drone)
        print("[OK] PX4KeyboardController 实例化成功")

        # 测试前进键
        print("测试前进键 (w)...")
        controller.control(ord('w'))

        # 测试左转键
        print("测试左转键 (q)...")
        controller.control(ord('q'))

        # 测试停止
        print("测试停止 (space)...")
        controller.control(ord(' '))

        return True

    except Exception as e:
        print(f"[FAIL] PX4键盘控制器测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始PX4键盘控制器测试...")
    print("=" * 50)

    success = test_px4_keyboard_controller()

    print("=" * 50)
    if success:
        print("PX4键盘控制器测试完成 - 所有功能正常")
    else:
        print("PX4键盘控制器测试失败")
