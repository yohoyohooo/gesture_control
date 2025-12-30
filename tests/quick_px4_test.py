#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速PX4连接测试脚本
用于验证PX4 SITL是否正在运行以及MAVLink连接是否正常
"""

import sys
import time
import os

def test_px4_connection(connection_string="udp:127.0.0.1:14550", timeout=10):
    """测试PX4连接"""
    print(f"正在测试PX4连接: {connection_string}")
    print("-" * 50)

    try:
        # 尝试导入pymavlink
        from pymavlink import mavutil
        print("✓ pymavlink 导入成功")

        # 创建连接
        print("正在连接到PX4...")
        master = mavutil.mavlink_connection(connection_string)

        # 等待心跳包
        print("等待心跳包...")
        heartbeat = master.wait_heartbeat(timeout=timeout)

        if heartbeat:
            print("✓ 成功接收到心跳包!")
            print(f"  系统ID: {master.target_system}")
            print(f"  组件ID: {master.target_component}")
            print(f"  系统类型: {master.field('HEARTBEAT', 'type')}")
            print(f"  飞行模式: {mavutil.mode_string_v10(heartbeat)}")

            # 测试基本命令
            print("\n测试基本MAVLink命令...")

            # 请求参数
            master.mav.param_request_list_send(
                master.target_system, master.target_component
            )
            print("✓ 发送参数请求")

            # 接收一些消息
            msg = master.recv_match(type='PARAM_VALUE', blocking=True, timeout=5)
            if msg:
                print(f"✓ 接收到参数: {msg.param_id} = {msg.param_value}")
            else:
                print("⚠ 未接收到参数响应")

            return True, master

        else:
            print("✗ 在超时时间内未接收到心跳包")
            print("\n可能的原因:")
            print("1. PX4 SITL没有启动")
            print("2. 连接字符串不正确")
            print("3. 防火墙阻止了UDP连接")
            print("4. 端口被其他程序占用")
            return False, None

    except ImportError:
        print("✗ pymavlink 未安装")
        print("请运行: pip install pymavlink")
        return False, None

    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False, None

def test_basic_commands(master):
    """测试基本飞行命令"""
    if not master:
        return

    print("\n测试基本飞行命令...")
    try:
        # 测试获取电池状态
        master.mav.request_data_stream_send(
            master.target_system, master.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1
        )
        print("✓ 请求数据流")

        # 等待一秒接收消息
        time.sleep(1)
        msg = master.recv_match(blocking=False)
        if msg:
            print(f"✓ 接收到消息: {msg.get_type()}")
        else:
            print("⚠ 未接收到数据流消息")

    except Exception as e:
        print(f"✗ 命令测试失败: {e}")

def main():
    print("PX4快速连接测试工具")
    print("=" * 60)

    # 默认连接字符串
    default_connection = "udp:127.0.0.1:14550"

    # 允许用户指定连接字符串
    if len(sys.argv) > 1:
        connection_string = sys.argv[1]
    else:
        connection_string = default_connection

    print(f"使用连接字符串: {connection_string}")
    print()

    # 测试连接
    success, master = test_px4_connection(connection_string)

    if success:
        # 测试基本命令
        test_basic_commands(master)

        print("\n" + "=" * 60)
        print("🎉 PX4连接测试成功!")
        print("\n现在你可以运行手势识别程序:")
        print("python main.py")
        print("\n或者指定连接字符串:")
        print(f"python main.py --px4_connection_string {connection_string}")

    else:
        print("\n" + "=" * 60)
        print("❌ PX4连接测试失败")
        print("\n请确保:")
        print("1. PX4 SITL正在运行")
        print("2. 连接字符串正确")
        print("3. 防火墙允许UDP连接")
        print("\n启动SITL命令:")
        print("cd ~/px4_ws/PX4-Autopilot && make px4_sitl gazebo")

if __name__ == "__main__":
    main()
