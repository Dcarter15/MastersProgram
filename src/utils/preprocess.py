import cv2
import numpy as np

def preprocess_frame(frame):
    if frame is None or frame.size == 0:
        return np.zeros((480, 640, 3), dtype=np.uint8)
    frame = cv2.resize(frame, (640, 480))
    return frame