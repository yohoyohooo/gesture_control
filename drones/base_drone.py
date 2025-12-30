from abc import ABC, abstractmethod

class BaseDrone(ABC):
    """无人机抽象基类，定义统一接口"""
    
    @abstractmethod
    def connect(self) -> bool:
        """连接无人机，返回是否成功"""
        pass
    
    @abstractmethod
    def streamon(self) -> None:
        """开启视频流"""
        pass
    
    @abstractmethod
    def get_frame_read(self):
        """获取视频帧读取对象"""
        pass
    
    @abstractmethod
    def takeoff(self) -> None:
        """起飞"""
        pass
    
    @abstractmethod
    def land(self) -> None:
        """降落"""
        pass
    
    @abstractmethod
    def move_forward(self, distance: int) -> None:
        """向前移动"""
        pass
    
    @abstractmethod
    def move_back(self, distance: int) -> None:
        """向后移动"""
        pass
    
    @abstractmethod
    def move_left(self, distance: int) -> None:
        """向左移动"""
        pass
    
    @abstractmethod
    def move_right(self, distance: int) -> None:
        """向右移动"""
        pass
    
    @abstractmethod
    def rotate_clockwise(self, degree: int) -> None:
        """顺时针旋转"""
        pass
    
    @abstractmethod
    def rotate_counter_clockwise(self, degree: int) -> None:
        """逆时针旋转"""
        pass
    
    @abstractmethod
    def move_up(self, distance: int) -> None:
        """向上移动"""
        pass
    
    @abstractmethod
    def move_down(self, distance: int) -> None:
        """向下移动"""
        pass
    
    @abstractmethod
    def send_rc_control(self, left_right: int, forw_back: int, up_down: int, yaw: int) -> None:
        """发送RC控制指令"""
        pass
    
    @abstractmethod
    def get_battery(self) -> str:
        """获取电池状态"""
        pass
    
    @abstractmethod
    def end(self) -> None:
        """断开连接"""
        pass