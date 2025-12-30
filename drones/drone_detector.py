from typing import Optional
from .tello_drone import TelloDrone
from .px4_drone import PX4Drone
from .base_drone import BaseDrone

class DroneDetector:
    @staticmethod
    def detect_and_connect(px4_connection_string: Optional[str] = None) -> BaseDrone:
        """自动识别并连接无人机，返回实例"""
        # 如果没有指定PX4连接字符串，使用默认值
        if px4_connection_string is None:
            px4_connection_string = "udp:127.0.0.1:14550"

        # 1. 尝试连接Tello
        print("尝试连接Tello无人机...")
        tello = TelloDrone()
        if tello.connect():
            print("成功连接Tello无人机")
            return tello

        # 2. 尝试连接PX4
        print(f"尝试连接PX4飞控... (连接字符串: {px4_connection_string})")
        px4 = PX4Drone(px4_connection_string)
        if px4.connect():
            print("成功连接PX4飞控")
            return px4

        # 3. 连接失败
        print("未识别到支持的无人机类型")
        return None