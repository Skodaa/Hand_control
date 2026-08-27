"""
How to use :
    python main.py              # no window, working in the background
    python main.py --debug      # window showing landmarks and gesture classification
"""
import argparse
import time

import config
from camera import Camera
from hand_tracker import HandTracker
from gesture_classifier import classify
from state_machine import StateMachine
import actions

from status_indicator import StatusIndicator


def run(debug=False):

    frame_interval = 1.0 / config.TARGET_FPS
    skip_counter = 0

    debug_view = None
    if debug:
        import debug_view as dv
        debug_view = dv

    with Camera() as cam, HandTracker() as tracker:

        sm = StateMachine()
        indicator = StatusIndicator()
        print("Program started")

        try:
            while True:
                loop_start = time.monotonic()

                frame = cam.read()
                if frame is None:
                    continue

                skip_counter += 1
                should_process = (skip_counter % (config.FRAME_SKIP + 1)) == 0

                if should_process:
                    landmarks = tracker.process(frame)
                    gesture = classify(landmarks)
                    action = sm.update(gesture)
                    indicator.set_state(sm.state)

                    if action:
                        actions.execute(action)
                        print(f"Action: {action}")

                    if debug_view:
                        debug_view.show(frame, landmarks, gesture, sm.state)

                elif debug_view:
                    debug_view.show(frame, None, None, sm.state)

                indicator.refresh()
                
                if debug_view and debug_view.should_quit():
                    break

                elapsed = time.monotonic() - loop_start
                sleep_time = frame_interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\nA Killing program")
        finally:
            indicator.close()
            if debug_view:
                debug_view.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Contrôle Spotify par gestes de la main.")
    parser.add_argument("--debug", action="store_true", help="Affiche une fenêtre de debug avec overlay.")
    args = parser.parse_args()

    run(debug=args.debug)
