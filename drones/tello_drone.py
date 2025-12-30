from djitellopy import Tello
from .base_drone import BaseDrone

class TelloDrone(BaseDrone):
    def __init__(self):
        self.tello = Tello()
        self.connected = False
    
    def connect(self) -> bool:
        try:
            self.tello.connect()
            self.connected = True
            return True
        except Exception as e:
            print(f"Tello连接失败: {e}")
            return False
    
    def streamon(self) -> None:
        if self.connected:
            self.tello.streamon()
    
    def get_frame_read(self):
        return self.tello.get_frame_read() if self.connected else None
    
    def takeoff(self) -> None:
        if self.connected:
            self.tello.takeoff()
    
    def land(self) -> None:
        if self.connected:
            self.tello.land()
    
    def move_forward(self, distance: int) -> None:
        if self.connected:
            self.tello.move_forward(distance)
    
    def move_back(self, distance: int) -> None:
        if self.connected:
            self.tello.move_back(distance)
    
    def move_left(self, distance: int) -> None:
        if self.connected:
            self.tello.move_left(distance)
    
    def move_right(self, distance: int) -> None:
        if self.connected:
            self.tello.move_right(distance)
    
    def rotate_clockwise(self, degree: int) -> None:
        if self.connected:
            self.tello.rotate_clockwise(degree)
    
    def rotate_counter_clockwise(self, degree: int) -> None:
        if self.connected:
            self.tello.rotate_counter_clockwise(degree)
    
    def move_up(self, distance: int) -> None:
        if self.connected:
            self.tello.move_up(distance)
    
    def move_down(self, distance: int) -> None:
        if self.connected:
            self.tello.move_down(distance)
    
    def send_rc_control(self, left_right: int, forw_back: int, up_down: int, yaw: int) -> None:
        if self.connected:
            self.tello.send_rc_control(left_right, forw_back, up_down, yaw)
    
    def get_battery(self) -> str:
        return str(self.tello.get_battery()) if self.connected else "N/A"
    
    def end(self) -> None:
        if self.connected:
            self.tello.end()