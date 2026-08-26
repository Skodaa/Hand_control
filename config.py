
# --- Camera configuration ---
CAMERA_INDEX = 0 # By default webcam is camera 0 but if infra red camera because super computer, might be 1
CAMERA_WIDTH = 384
CAMERA_HEIGHT = 216
TARGET_FPS = 15 # Frame taken by second, if your computer is like a war machine you can go for more but this works good
FRAME_SKIP = 1 # number of frame skipped (Better performance )

# --- MediaPipe ---
# NGL took those model configurations data on google but I of course understand those
MODEL_COMPLEXITY = 0 
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.5

# --- states gestion ---
ARM_HOLD_TIME = 0.2 # seconds where the hand is open to activate the action
ARM_TIMEOUT = 2.0 # number of seconds after system finds the open hand to make a move 
ACTION_CONFIRM_FRAMES = 3 # number of consecutive frame where the action should be the same 
COOLDOWN_TIME = 1.2 # seconds after the exsecution of the action to ensure it is not played multiple times 

# --- gesture classification ---
POINT_HORIZONTAL_THRESHOLD = 0.06  # Threshold used to help see if the finger points to the left or the right
POINT_VERTICAL_THRESHOLD = 0.10 
DIRECTION_BIAS = 1.3
THUMB_EXTENDED_RATIO = 0.6  

# --- Debug ---
DEBUG_DEFAULT = False # state of the debug mode
