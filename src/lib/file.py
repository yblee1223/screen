import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw
import os
import threading

def lastest_file():
    input_path = os.path.join(".", "data", "input")

    dir = sorted(os.listdir(input_path))
    if len(dir) == 0:
        print('ERROR: NO files exist in input dir')
        return False
    
    lastest_timestr = sorted([file.split('_')[-1].split('.')[0] for file in dir])[-1]
    for file_name in dir:
        if lastest_timestr in file_name:
            return file_name

def screen_capture(title_name):
    all_title = gw.getAllTitles()
    title = [file for file in all_title if ("Level" in file)]

    if not title:
        print("No window with 'Level' in the title found!")
        exit()

    window = gw.getWindowsWithTitle(title[0])[0]
    left, top, width, height = window.left, window.top, window.width, window.height

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f"{title_name}.mp4", fourcc, 20.0, (width, height))

    return out

def capturing():

    while True:
        # 창 영역 캡처
        img = pyautogui.screenshot(region=(left, top, width, height))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 캡처한 프레임을 파일에 작성
        out.write(frame)
        
        # ESC 키를 누르면 레코딩 종료
        if cv2.waitKey(1) == 27:
            break
        
        # 설정된 시간 동안 녹화 후 종료
        if time.time() - start_time > record_seconds:
            break

    # 리소스 해제
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print(lastest_file())