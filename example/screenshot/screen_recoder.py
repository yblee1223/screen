import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time

all_title = gw.getAllTitles()

title = [file for file in all_title if ("Level" in file)]

print(title[0])
window = gw.getWindowsWithTitle(title[0])
print(window.width)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("window_record.mp4", fourcc, 20.0, (1920, 1080))

start_time = time.time()
record_seconds = 10

while True:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('frame', frame)

    out.write(frame)
    
    if cv2.waitKey(1) == 27:
        break
    
    if time.time() - start_time > record_seconds:
        break

# 리소스 해제
out.release()
cv2.destroyAllWindows()
