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
        
class ScreenRecorder:
    def __init__(self) -> None:
        self.__running = False
        self.video_folder = os.path.join('data', 'video')
        if not os.path.exists(self.video_folder):
            os.mkdir(self.video_folder)
    
    def _start_recording(self, video_name:str) -> None:
        time.sleep(10)
        self.__running = True
        all_title = gw.getAllTitles()
        title = [file for file in all_title if ("Level" in file)]

        if not title:
            print("ERROR: No window with 'Level' in the title found!")
            return None
        window = gw.getWindowsWithTitle(title[0])[0]
        left, top, width, height = window.left, window.top, window.width, window.height

        fourcc = cv2.VideoWriter_fourcc(*'X264')
        out = cv2.VideoWriter(os.path.join(self.video_folder, f"{video_name}.mp4"), fourcc, 30.0, (width, height))

        while self.__running:
            img = pyautogui.screenshot(region=(left, top, width, height))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            out.write(frame)

            if cv2.waitKey(1) == 27:
                break
        
        out.release()
    
    def start_recording(self, video_name:str) -> None:
        t = threading.Thread(target=self._start_recording, args=(video_name,))
        t.start()

    def stop_recording(self) -> None:
        self.__running = False
        cv2.destroyAllWindows()



if __name__ == "__main__":
    print(lastest_file())
    recorder = ScreenRecorder()
    threading.Thread(target=recorder.start_recording, args=["hello",]).start()
    time.sleep(10)
    threading.Thread(target=recorder.stop_recording, args=[]).start()
