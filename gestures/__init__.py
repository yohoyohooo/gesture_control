# 按需导入，避免在包初始化时加载所有依赖
__all__ = [
    'GestureRecognition',
    'GestureBuffer',
    'TelloGestureController',
    'TelloKeyboardController',
    'PX4GestureController',
    'PX4KeyboardController'
]

def __getattr__(name):
    if name == 'GestureRecognition':
        from gestures.gesture_recognition import GestureRecognition
        return GestureRecognition
    elif name == 'GestureBuffer':
        from gestures.gesture_recognition import GestureBuffer
        return GestureBuffer
    elif name == 'TelloGestureController':
        from gestures.tello_gesture_controller import TelloGestureController
        return TelloGestureController
    elif name == 'TelloKeyboardController':
        from gestures.tello_keyboard_controller import TelloKeyboardController
        return TelloKeyboardController
    elif name == 'PX4GestureController':
        from gestures.px4_gesture_controller import PX4GestureController
        return PX4GestureController
    elif name == 'PX4KeyboardController':
        from gestures.px4_keyboard_controller import PX4KeyboardController
        return PX4KeyboardController
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
