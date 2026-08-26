from pynput.keyboard import Controller, Key

_keyboard = Controller()

_KEY_MAP = {
    "play_pause": Key.media_play_pause, # Start / pause the current media
    "next": Key.media_next, # yeet that sh*t and go to next media
    "previous": Key.media_previous, # go back to the start / to the previous media
}


def execute(action):
    """ Simulate an input of a key from the keys map"""
    key = _KEY_MAP.get(action)
    if key is None:
        return
    _keyboard.press(key)
    _keyboard.release(key)
