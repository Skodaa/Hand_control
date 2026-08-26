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


def classify(landmarks):
    """ Classify the current gesture using the different points and the finger map"""

    if landmarks is None:
        return "none"

    extended = {name: _is_extended(landmarks, name) for name in FINGERS}

    # We don't use the thumb because for a next update it will be annoying me ngl
    non_thumb = [extended[name] for name in ("index", "fuck", "near_fuck", "little")]
    nb_non_thumb_extended = sum(non_thumb)

    if nb_non_thumb_extended == 4:
        return "palm_open"

    if nb_non_thumb_extended == 0:
        return "fist"

    # Ugly way to check if index is pointing in a direction (for now)
    others_folded = not extended["fuck"] and not extended["near_fuck"] and not extended["little"]
    if extended["index"] and others_folded:
        return _point_direction(landmarks)

    return "none"


def _point_direction(landmarks):
    """ Check the direction the finger is pointing at"""

    wrist = landmarks[WRIST]
    index_tip = landmarks[FINGERS["index"]["tip"]]

    dx = index_tip[0] - wrist[0]
    dy = index_tip[1] - wrist[1]

    # for now up and down are not mapped so just don't care
    if abs(dx) < config.POINT_HORIZONTAL_THRESHOLD * max(abs(dy), 0.01) and abs(dx) < config.POINT_HORIZONTAL_THRESHOLD:
        return "none"

    # Taking in account camera mirroring real life cause it stinks, dx > 0 = right but then mirrored it is really just left
    if dx > 0:
        return "point_left"
    else:
        return "point_right"
