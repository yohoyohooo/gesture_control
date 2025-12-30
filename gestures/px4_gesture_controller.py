from drones.base_drone import BaseDrone  # 依赖抽象类

class PX4GestureController:
    def __init__(self, drone: BaseDrone):
        self.drone = drone
        self._is_landing = False

        # RC control velocities (PX4通常比Tello更敏感，使用较低的速度)
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.left_right_velocity = 0
        self.yaw_velocity = 0

        # PX4特定的参数
        self.max_velocity = 30  # 最大速度限制

    def gesture_control(self, gesture_buffer):
        """处理手势控制逻辑"""
        gesture_id = gesture_buffer.get_gesture()
        print("PX4 GESTURE", gesture_id)

        if not self._is_landing:
            if gesture_id == 0:  # Forward - 降低速度以适应PX4
                self.forw_back_velocity = min(20, self.max_velocity)
            elif gesture_id == 1:  # STOP
                self.forw_back_velocity = self.up_down_velocity = \
                    self.left_right_velocity = self.yaw_velocity = 0
            elif gesture_id == 5:  # Back
                self.forw_back_velocity = max(-20, -self.max_velocity)

            elif gesture_id == 2:  # UP - PX4上升更平滑
                self.up_down_velocity = min(15, self.max_velocity)
            elif gesture_id == 4:  # DOWN
                self.up_down_velocity = max(-15, -self.max_velocity)

            elif gesture_id == 3:  # LAND
                self._is_landing = True
                self.forw_back_velocity = self.up_down_velocity = \
                    self.left_right_velocity = self.yaw_velocity = 0
                self.drone.land()

            elif gesture_id == 6:  # LEFT
                self.left_right_velocity = min(15, self.max_velocity)
            elif gesture_id == 7:  # RIGHT
                self.left_right_velocity = max(-15, -self.max_velocity)

            elif gesture_id == -1:  # No gesture detected
                # 逐渐减速而不是立即停止
                self._gradual_stop()

            # 发送RC控制指令
            self.drone.send_rc_control(
                self.left_right_velocity,
                self.forw_back_velocity,
                self.up_down_velocity,
                self.yaw_velocity
            )

    def _gradual_stop(self):
        """逐渐减速到停止，提供更平滑的控制"""
        decay_rate = 0.8  # 每次减少20%

        self.forw_back_velocity *= decay_rate
        self.up_down_velocity *= decay_rate
        self.left_right_velocity *= decay_rate
        self.yaw_velocity *= decay_rate

        # 如果速度很小，直接设置为0
        threshold = 1.0
        if abs(self.forw_back_velocity) < threshold:
            self.forw_back_velocity = 0
        if abs(self.up_down_velocity) < threshold:
            self.up_down_velocity = 0
        if abs(self.left_right_velocity) < threshold:
            self.left_right_velocity = 0
        if abs(self.yaw_velocity) < threshold:
            self.yaw_velocity = 0

    def emergency_stop(self):
        """紧急停止"""
        self.forw_back_velocity = self.up_down_velocity = \
            self.left_right_velocity = self.yaw_velocity = 0
        self.drone.send_rc_control(0, 0, 0, 0)
        print("PX4紧急停止")

    def reset_landing_flag(self):
        """重置着陆标志"""
        self._is_landing = False
