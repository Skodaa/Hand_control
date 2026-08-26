"""Function to evaluate the gesture using the points of mediapip"""
import math
import config

WRIST = 0
# Mapping of the different fingers using the points
FINGERS = {
    "thumb": {"pip": 2, "tip": 4}, 
    "index": {"pip": 6, "tip": 8},
    "fuck": {"pip": 10, "tip": 12},
    "near_fuck": {"pip": 14, "tip": 16},
    "little": {"pip": 18, "tip": 20},
}


def _dist(a, b):

    return math.hypot(a[0] - b[0], a[1] - b[1])


def _is_extended(landmarks, finger_name):
    """ Check if the given finger is straight"""

    wrist = landmarks[WRIST]
    pip = landmarks[FINGERS[finger_name]["pip"]]
    tip = landmarks[FINGERS[finger_name]["tip"]]

    return _dist(wrist, tip) > _dist(wrist, pip)

def _is_thumb_extended(landmarks):

    wrist = landmarks[WRIST]
    thumb_tip = landmarks[4]
    index_mcp = landmarks[5]
    pinky_mcp = landmarks[17]

    palm_width = _dist(index_mcp, pinky_mcp)
    if palm_width < 1e-6:
        return False

    thumb_spread = _dist(thumb_tip, index_mcp)
    ratio = thumb_spread / palm_width

    return ratio > config.THUMB_EXTENDED_RATIO


def classify(landmarks):
    """ Classify the current gesture using the different points and the finger map"""

    if landmarks is None:
        return "none"

    extended = {name: _is_extended(landmarks, name) for name in FINGERS if name != "thumb"}
    extended["thumb"] = _is_thumb_extended(landmarks)

    # We don't use the thumb because for a next update it will be annoying me ngl
    non_thumb = [extended[name] for name in ("index", "fuck", "near_fuck", "little")]
    nb_non_thumb_extended = sum(non_thumb)

    if nb_non_thumb_extended == 4:
        return "palm_open"

    others_folded = (
        not extended["index"]
        and not extended["fuck"]
        and not extended["near_fuck"]
        and not extended["little"]
    )
    if extended["thumb"] and others_folded:
        return _point_direction(landmarks)

    if nb_non_thumb_extended == 0 and not extended["thumb"]:
        return "fist"

    return "none"


def _point_direction(landmarks):
    """ Check the direction the finger is pointing at"""

    index_mcp = landmarks[5]
    thumb_tip = landmarks[FINGERS["thumb"]["tip"]]

    dx = thumb_tip[0] - index_mcp[0]
    dy = thumb_tip[1] - index_mcp[1]

    if abs(dx) > abs(dy) * config.DIRECTION_BIAS:

        if abs(dx) < config.POINT_HORIZONTAL_THRESHOLD:
            return "none"
        
        return "point_left" if dx > 0 else "point_right"

    else:

        if abs(dy) < config.POINT_VERTICAL_THRESHOLD:
            return "none"

        return "point_down" if dy > 0 else "point_up"
