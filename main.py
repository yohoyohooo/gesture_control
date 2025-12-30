#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configargparse

import cv2 as cv

from utils import CvFpsCalc
from drones.drone_detector import DroneDetector

from drones.tello_drone import TelloDrone
from drones.px4_drone import PX4Drone

from gestures import *
from gestures.tello_gesture_controller import TelloGestureController
from gestures.px4_gesture_controller import PX4GestureController
from gestures.px4_keyboard_controller import PX4KeyboardController

import threading


def get_args():
    print('## Reading configuration ##')
    parser = configargparse.ArgParser(default_config_files=['config.txt'])

    parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    parser.add("--device", type=int)
    parser.add("--width", help='cap width', type=int)
    parser.add("--height", help='cap height', type=int)
    parser.add("--is_keyboard", help='To use Keyboard control by default', type=bool)
    parser.add('--use_static_image_mode', action='store_true', help='True if running on photos')
    parser.add("--min_detection_confidence",
               help='min_detection_confidence',
               type=float)
    parser.add("--min_tracking_confidence",
               help='min_tracking_confidence',
               type=float)
    parser.add("--buffer_len",
               help='Length of gesture buffer',
               type=int)
    parser.add("--px4_connection_string",
               help='PX4 MAVLink connection string (e.g., udp:127.0.0.1:14550)',
               type=str)

    args = parser.parse_args()

    return args


def select_mode(key, mode):
    number = -1
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1
    if key == 104:  # h
        mode = 2
    return number, mode


def main():
    # init global vars
    global gesture_buffer
    global gesture_id
    global battery_status

    # Argument parsing
    args = get_args()
    KEYBOARD_CONTROL = args.is_keyboard
    WRITE_CONTROL = False
    in_flight = False

    # Camera preparation
    # 使用configargparse自动处理的PX4连接字符串参数（来自命令行或config.txt）
    drone = DroneDetector.detect_and_connect(args.px4_connection_string)
    if not drone:
        print("无人机连接失败，退出程序")
        exit(1)
    drone.streamon()

    cap = drone.get_frame_read()

    # 根据无人机类型初始化相应的控制器
    drone_type = type(drone).__name__
    print(f"检测到无人机类型: {drone_type}")

    if drone_type == "TelloDrone":
        gesture_controller = TelloGestureController(drone)
        keyboard_controller = TelloKeyboardController(drone)
    elif drone_type == "PX4Drone":
        gesture_controller = PX4GestureController(drone)
        keyboard_controller = PX4KeyboardController(drone)
        print("PX4无人机支持手势和键盘控制模式")
    else:
        print(f"不支持的无人机类型: {drone_type}")
        exit(1)

    gesture_detector = GestureRecognition(args.use_static_image_mode, args.min_detection_confidence,
                                          args.min_tracking_confidence)
    gesture_buffer = GestureBuffer(buffer_len=args.buffer_len)

    def drone_control(key, keyboard_controller, gesture_controller, drone_type):
        global gesture_buffer

        if KEYBOARD_CONTROL:
            if keyboard_controller:
                keyboard_controller.control(key)
            else:
                print("当前无人机类型不支持键盘控制")
        else:
            gesture_controller.gesture_control(gesture_buffer)

    def drone_battery(drone):
        global battery_status
        try:
            battery_status = drone.get_battery()[:-2]
        except:
            battery_status = -1

    # FPS Measurement
    cv_fps_calc = CvFpsCalc(buffer_len=10)

    mode = 0
    number = -1
    battery_status = -1

    drone.move_down(20)

    while True:
        fps = cv_fps_calc.get()

        # Process Key (ESC: end)
        key = cv.waitKey(1) & 0xff
        if key == 27:  # ESC
            break
        elif key == 32:  # Space
            if not in_flight:
                # Take-off drone
                drone.takeoff()
                in_flight = True

            elif in_flight:
                # Land tello
                drone.land()
                in_flight = False

        elif key == ord('k'):
            mode = 0
            KEYBOARD_CONTROL = True
            WRITE_CONTROL = False
            drone.send_rc_control(0, 0, 0, 0)  # Stop moving
        elif key == ord('g'):
            KEYBOARD_CONTROL = False
        elif key == ord('n'):
            mode = 1
            WRITE_CONTROL = True
            KEYBOARD_CONTROL = True

        if WRITE_CONTROL:
            number = -1
            if 48 <= key <= 57:  # 0 ~ 9
                number = key - 48

        # Camera capture
        image = cap.frame

        debug_image, gesture_id = gesture_detector.recognize(image, number, mode)
        gesture_buffer.add_gesture(gesture_id)

        # Start control thread
        threading.Thread(target=drone_control, args=(key, keyboard_controller, gesture_controller, drone_type,)).start()
        threading.Thread(target=drone_battery, args=(drone,)).start()

        debug_image = gesture_detector.draw_info(debug_image, fps, mode, number)

        # Battery status and image rendering
        cv.putText(debug_image, "Battery: {}".format(battery_status), (5, 720 - 5),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv.imshow('Tello Gesture Recognition', debug_image)

    drone.land()
    drone.end()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
