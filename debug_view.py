""" Debug window that show everything the system sees"""

import cv2

_WINDOW_NAME = "Hand Gesture Debug"

_STATE_COLORS = {
    "IDLE": (128, 128, 128),
    "ARMED": (0, 200, 255),
    "COOLDOWN": (0, 0, 255),
}

_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),          # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),          # index
    (0, 9), (9, 10), (10, 11), (11, 12),     # the fuck finger
    (0, 13), (13, 14), (14, 15), (15, 16),   # fuck finger little brother
    (0, 17), (17, 18), (18, 19), (19, 20),   # little finger
]


def show(frame, landmarks, gesture, state):
    display = frame.copy()
    h, w = display.shape[:2]

    if landmarks:
        points = [(int(x * w), int(y * h)) for x, y, _ in landmarks]
        for a, b in _CONNECTIONS:
            cv2.line(display, points[a], points[b], (0, 255, 0), 1)
        for p in points:
            cv2.circle(display, p, 3, (0, 255, 0), -1)

    color = _STATE_COLORS.get(state, (255, 255, 255))
    cv2.putText(display, f"State: {state}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    if gesture:
        cv2.putText(display, f"Gesture: {gesture}", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow(_WINDOW_NAME, display)
    cv2.waitKey(1)


def should_quit():
    """ close the window with the top right hand corner cross"""
    try:
        return cv2.getWindowProperty(_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1
    except cv2.error:
        return False


def cleanup():
    cv2.destroyAllWindows()
