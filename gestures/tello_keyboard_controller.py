from drones.base_drone import BaseDrone
class TelloKeyboardController:
    def __init__(self, drone: BaseDrone):
        self.drone = drone

    def control(self, key):
        if key == ord('w'):
            self.drone.move_forward(30)
        elif key == ord('s'):
            self.drone.move_back(30)
        elif key == ord('a'):
            self.drone.move_left(30)
        elif key == ord('d'):
            self.drone.move_right(30)
        elif key == ord('e'):
            self.drone.rotate_clockwise(30)
        elif key == ord('q'):
            self.drone.rotate_counter_clockwise(30)
        elif key == ord('r'):
            self.drone.move_up(30)
        elif key == ord('f'):
            self.drone.move_down(30)



