import time
import threading
from typing import Optional
from .base_drone import BaseDrone

try:
    from pymavlink import mavutil
    from pymavlink.mavutil import mavlink_connection
    MAVLINK_AVAILABLE = True
except ImportError:
    MAVLINK_AVAILABLE = False
    print("警告: pymavlink未安装，PX4无人机功能不可用")


class PX4Drone(BaseDrone):
    def __init__(self, connection_string: str = "udp:127.0.0.1:14550"):
        """
        初始化PX4无人机
        Args:
            connection_string: MAVLink连接字符串，如"udp:127.0.0.1:14550"或串口"COM3:57600"
        """
        self.connected = False
        self.connection_string = connection_string
        self.master: Optional[mavlink_connection] = None
        self.heartbeat_thread: Optional[threading.Thread] = None
        self.stop_heartbeat = False
        self.last_heartbeat = 0
        self.mode = "MANUAL"
        self.armed = False
        self.system_status = 0

        # 视频流相关（PX4通常需要外部摄像头）
        self.video_stream_active = False
        self.cap = None

        if not MAVLINK_AVAILABLE:
            print("错误: 无法使用PX4功能，请安装pymavlink: pip install pymavlink")
            return

    def connect(self) -> bool:
        """连接到PX4飞控"""
        try:
            print(f"正在连接到PX4: {self.connection_string}")
            self.master = mavutil.mavlink_connection(self.connection_string)

            # 等待心跳包
            print("等待PX4心跳包...")
            self.master.wait_heartbeat(timeout=10)

            print(f"连接成功! 系统ID: {self.master.target_system}, 组件ID: {self.master.target_component}")

            # 启动心跳监听线程
            self.heartbeat_thread = threading.Thread(target=self._heartbeat_listener)
            self.heartbeat_thread.daemon = True
            self.heartbeat_thread.start()

            # 请求数据流
            self._request_data_streams()

            self.connected = True
            return True

        except Exception as e:
            print(f"PX4连接失败: {e}")
            return False

    def _heartbeat_listener(self):
        """监听心跳包和系统状态"""
        while not self.stop_heartbeat and self.master:
            try:
                msg = self.master.recv_match(type='HEARTBEAT', blocking=False, timeout=1)
                if msg:
                    self.last_heartbeat = time.time()
                    self.mode = mavutil.mode_string_v10(msg)
                    self.armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    self.system_status = msg.system_status

                # 检查连接是否仍然有效
                if time.time() - self.last_heartbeat > 5:
                    print("警告: PX4心跳超时，可能失去连接")
                    self.connected = False

            except Exception as e:
                print(f"心跳监听错误: {e}")
                time.sleep(1)

    def _request_data_streams(self):
        """请求数据流"""
        try:
            # 请求所有数据流
            self.master.mav.request_data_stream_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_DATA_STREAM_ALL,
                4,  # 4Hz
                1   # 启用
            )
        except Exception as e:
            print(f"请求数据流失败: {e}")

    def streamon(self) -> None:
        """开启视频流（PX4通常需要外部摄像头）"""
        if self.connected:
            try:
                import cv2 as cv
                # PX4本身不提供视频流，通常需要外部摄像头
                # 这里假设使用默认摄像头，或者可以配置特定的摄像头
                self.cap = cv.VideoCapture(0)  # 使用默认摄像头
                if self.cap.isOpened():
                    self.video_stream_active = True
                    print("PX4视频流已开启（外部摄像头）")
                else:
                    print("警告: 无法开启视频流，请检查摄像头连接")
            except Exception as e:
                print(f"开启视频流失败: {e}")

    def get_frame_read(self):
        """获取视频帧读取对象"""
        if self.video_stream_active and self.cap:
            return self.cap
        return None

    def takeoff(self) -> None:
        """起飞"""
        if not self.connected:
            return

        try:
            # 切换到GUIDED模式
            self._set_mode("GUIDED")

            # 等待模式切换
            time.sleep(1)

            # 发送起飞命令
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0,  # confirmation
                0, 0, 0, 0,  # param1-4 (unused)
                0, 0, 10.0   # param5-7: lat, lon, alt (10m)
            )
            print("PX4起飞命令已发送")

        except Exception as e:
            print(f"PX4起飞失败: {e}")

    def land(self) -> None:
        """降落"""
        if not self.connected:
            return

        try:
            # 发送降落命令
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_LAND,
                0,  # confirmation
                0, 0, 0, 0,  # param1-4 (unused)
                0, 0, 0      # param5-7: lat, lon, alt (unused)
            )
            print("PX4降落命令已发送")

        except Exception as e:
            print(f"PX4降落失败: {e}")

    def move_forward(self, distance: int) -> None:
        """向前移动指定距离(cm)"""
        if not self.connected:
            return

        try:
            # 在GUIDED模式下发送位置偏移命令
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT,
                0,
                0, distance/100.0, 0, 0,  # 前进距离（米）
                0, 0, 0
            )
        except Exception as e:
            print(f"PX4前进失败: {e}")

    def move_back(self, distance: int) -> None:
        """向后移动指定距离(cm)"""
        self.move_forward(-distance)

    def move_left(self, distance: int) -> None:
        """向左移动指定距离(cm)"""
        if not self.connected:
            return

        try:
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT,
                0,
                -distance/100.0, 0, 0, 0,  # 左移距离（米）
                0, 0, 0
            )
        except Exception as e:
            print(f"PX4左移失败: {e}")

    def move_right(self, distance: int) -> None:
        """向右移动指定距离(cm)"""
        self.move_left(-distance)

    def rotate_clockwise(self, degree: int) -> None:
        """顺时针旋转指定角度"""
        if not self.connected:
            return

        try:
            # 发送偏航角改变命令
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_CONDITION_YAW,
                0,
                degree,  # 偏航角度
                0,       # 偏航速度
                1,       # 相对角度（1=相对，0=绝对）
                0, 0, 0
            )
        except Exception as e:
            print(f"PX4顺时针旋转失败: {e}")

    def rotate_counter_clockwise(self, degree: int) -> None:
        """逆时针旋转指定角度"""
        self.rotate_clockwise(-degree)

    def move_up(self, distance: int) -> None:
        """向上移动指定距离(cm)"""
        if not self.connected:
            return

        try:
            # 发送上升命令
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0,
                0, 0, 0, 0,
                0, 0, distance/100.0  # 上升高度（米）
            )
        except Exception as e:
            print(f"PX4上升失败: {e}")

    def move_down(self, distance: int) -> None:
        """向下移动指定距离(cm)"""
        self.move_up(-distance)

    def send_rc_control(self, left_right: int, forw_back: int, up_down: int, yaw: int) -> None:
        """发送RC控制指令（范围-100到100）"""
        if not self.connected:
            return

        try:
            # 将输入范围(-100,100)转换为MAVLink RC通道范围(1000-2000)
            def scale_rc(value):
                return int(1500 + value * 5)  # 1500为中心，±500范围

            rc_channels = [
                scale_rc(left_right),   # 通道1: 横滚
                scale_rc(forw_back),    # 通道2: 俯仰
                scale_rc(up_down),      # 通道3: 油门
                scale_rc(yaw),          # 通道4: 偏航
                1500, 1500, 1500, 1500  # 其他通道居中
            ]

            self.master.mav.rc_channels_override_send(
                self.master.target_system,
                self.master.target_component,
                *rc_channels
            )

        except Exception as e:
            print(f"PX4 RC控制失败: {e}")

    def get_battery(self) -> str:
        """获取电池状态"""
        if not self.connected:
            return "N/A"

        try:
            # 尝试获取电池状态消息
            msg = self.master.recv_match(type='BATTERY_STATUS', blocking=False)
            if msg:
                voltage = msg.voltages[0] / 1000.0 if msg.voltages else 0
                return f"{voltage:.1f}V"
            return "未知"
        except Exception as e:
            print(f"获取电池状态失败: {e}")
            return "N/A"

    def _set_mode(self, mode: str):
        """设置飞行模式"""
        if not self.connected:
            return

        try:
            # 获取模式的MAVLink常量
            mode_mapping = {
                "MANUAL": mavutil.mavlink.MAV_MODE_MANUAL_ARMED,
                "GUIDED": mavutil.mavlink.MAV_MODE_GUIDED_ARMED,
                "AUTO": mavutil.mavlink.MAV_MODE_AUTO_ARMED,
            }

            if mode in mode_mapping:
                mode_id = mode_mapping[mode]
                self.master.mav.set_mode_send(
                    self.master.target_system,
                    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                    mode_id
                )
                print(f"设置PX4模式为: {mode}")
            else:
                print(f"未知模式: {mode}")

        except Exception as e:
            print(f"设置模式失败: {e}")

    def end(self) -> None:
        """断开连接"""
        self.connected = False
        self.stop_heartbeat = True

        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            self.heartbeat_thread.join(timeout=2)

        if self.cap:
            self.cap.release()

        if self.master:
            try:
                self.master.close()
            except:
                pass

        print("PX4连接已断开")