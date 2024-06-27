import numpy as np
import cv2
from mss import mss
from PIL import Image

sct = mss()

while True:
    sct_img = sct.grab(sct.monitors[0])
    cv2.imshow('screen', np.array(sct_img))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
