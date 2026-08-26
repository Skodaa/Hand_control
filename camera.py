import cv2
import config


class Camera:
    """ Class to control the camera flow
    """
    def __init__(self):

        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera : (index %d)" % config.CAMERA_INDEX)

    def read(self):
        
        ok, frame = self.cap.read()

        if not ok:
            return None
        return frame

    def release(self):

        self.cap.release()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.release()
