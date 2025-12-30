from drones.base_drone import BaseDrone

class PX4KeyboardController:
    def __init__(self, drone: BaseDrone):
        self.drone = drone
        # PX4 RC控制参数
        self.left_right_velocity = 0
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0

    def control(self, key):
        """处理键盘控制输入"""
        # 重置速度
        self.left_right_velocity = 0
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0

        if key == ord('w'):
            self.forw_back_velocity = 20  # 前进
            print("PX4: 前进")
        elif key == ord('s'):
            self.forw_back_velocity = -20  # 后退
            print("PX4: 后退")
        elif key == ord('a'):
            self.left_right_velocity = -20  # 左移
            print("PX4: 左移")
        elif key == ord('d'):
            self.left_right_velocity = 20  # 右移
            print("PX4: 右移")
        elif key == ord('q'):
            self.yaw_velocity = -15  # 左转
            print("PX4: 左转")
        elif key == ord('e'):
            self.yaw_velocity = 15  # 右转
            print("PX4: 右转")
        elif key == ord('r'):
            self.up_down_velocity = 15  # 上升
            print("PX4: 上升")
        elif key == ord('f'):
            self.up_down_velocity = -15  # 下降
            print("PX4: 下降")
        elif key == ord(' '):  # 空格键
            # 紧急停止
            self.left_right_velocity = 0
            self.forw_back_velocity = 0
            self.up_down_velocity = 0
            self.yaw_velocity = 0
            print("PX4: 紧急停止")

        # 发送RC控制指令
        self.drone.send_rc_control(
            self.left_right_velocity,
            self.forw_back_velocity,
            self.up_down_velocity,
            self.yaw_velocity
        )
