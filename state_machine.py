import time
import config

# Different state of the hand gesture recognition
IDLE = "IDLE"
ARMED = "ARMED"
COOLDOWN = "COOLDOWN"

# Different possible actions
ACTION_GESTURES = {
    "fist": "play_pause",
    "point_left": "previous",
    "point_right": "next",
}

CONTINUOUS_GESTURES = {
    "point_up": "volume_up",
    "point_down": "volume_down",
}


class StateMachine:
    
    def __init__(self):

        self.state = IDLE
        self._palm_hold_start = None      # first freale where palm is seen
        self._armed_at = None             # moment when system is armed
        self._cooldown_until = None       # moment where we force disarm the system
        self._confirm_gesture = None      # Gesture we try to confirm
        self._confirm_count = 0           # consecutive frames where the gesture have been recognized

    def update(self, gesture):
        
        now = time.monotonic()

        if self.state == IDLE:
            self._handle_idle(gesture, now)
            return None

        if self.state == ARMED:
            return self._handle_armed(gesture, now)

        if self.state == COOLDOWN:
            self._handle_cooldown(now)
            return None

        return None


    def _handle_idle(self, gesture, now):

        if gesture == "palm_open":

            if self._palm_hold_start is None:
                self._palm_hold_start = now

            elif now - self._palm_hold_start >= config.ARM_HOLD_TIME:
                self._enter_armed(now)

        else:
            self._palm_hold_start = None

    def _handle_armed(self, gesture, now):

        # if max time to wait is reached we disarm isra.. the system.. sadly just the system...
        if now - self._armed_at > config.ARM_TIMEOUT:
            self._enter_idle()
            return None

        if gesture in CONTINUOUS_GESTURES:
            if gesture == self._confirm_gesture:
                self._confirm_count += 1
            else:
                self._confirm_gesture = gesture
                self._confirm_count = 1

            self._armed_at = now

            if self._confirm_count >= config.ACTION_CONFIRM_FRAMES:
                return CONTINUOUS_GESTURES[gesture]
            return None

        if gesture in ACTION_GESTURES:

            if gesture == self._confirm_gesture:
                self._confirm_count += 1
            else:
                self._confirm_gesture = gesture
                self._confirm_count = 1

            if self._confirm_count >= config.ACTION_CONFIRM_FRAMES:
                action = ACTION_GESTURES[gesture]
                self._enter_cooldown(now)
                return action
        else:
            # if the gesture changed for oen frame we continue to check because it can be an error
            self._confirm_gesture = None
            self._confirm_count = 0

        return None

    def _handle_cooldown(self, now):

        if now >= self._cooldown_until:
            self._enter_idle()

    def _enter_armed(self, now):

        self.state = ARMED
        self._armed_at = now
        self._palm_hold_start = None
        self._confirm_gesture = None
        self._confirm_count = 0

    def _enter_cooldown(self, now):

        self.state = COOLDOWN
        self._cooldown_until = now + config.COOLDOWN_TIME
        self._confirm_gesture = None
        self._confirm_count = 0

    def _enter_idle(self):
        
        self.state = IDLE
        self._palm_hold_start = None
        self._armed_at = None
        self._confirm_gesture = None
        self._confirm_count = 0
