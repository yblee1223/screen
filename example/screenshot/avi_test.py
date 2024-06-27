import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw

all_title = gw.getAllTitles()

title = [file for file in all_title if ("Level" in file)]

print(title)
window = gw.getWindowsWithTitle(title[0])
print(window)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("window_record.mp4", fourcc, 20.0, (1920, 1080))
# 스크린 사이즈 얻기
screen_size = pyautogui.size()

# 비디오 파일 저장을 위한 코덱 정의 및 VideoWriter 객체 생성
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("screen_record.avi", fourcc, 20.0, (screen_size.width, screen_size.height))

# 레코딩 시작
start_time = time.time()
record_seconds = 10  # 녹화할 시간(초)

while True:
    # 스크린 캡처
    img = pyautogui.screenshot()
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
