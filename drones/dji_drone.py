from .base_drone import BaseDrone

class DjiDrone(BaseDrone):
    def __init__(self):
        self.connected = False
    
    def connect(self) -> bool:
        try:
            self.connected = True
            return True
        except Exception as e:
            print(f"PX4连接失败: {e}")
            return False
    
    def streamon(self) -> None:
        if self.connected:
            pass
    