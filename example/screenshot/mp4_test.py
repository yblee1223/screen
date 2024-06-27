import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw

# 모든 창 제목 가져오기
all_title = gw.getAllTitles()

# "Level"이 포함된 창 제목 찾기
title = [file for file in all_title if ("Level" in file)]

if not title:
    print("No window with 'Level' in the title found!")
    exit()

print(title)

# 해당 창 가져오기
window = gw.getWindowsWithTitle(title[0])[0]
print(window)

# 창 위치와 크기 얻기
left, top, width, height = window.left, window.top, window.width, window.height

# 비디오 파일 저장을 위한 코덱 정의 및 VideoWriter 객체 생성 (MP4)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("window_record.mp4", fourcc, 20.0, (width, height))

# 레코딩 시작
start_time = time.time()
record_seconds = 10  # 녹화할 시간(초)

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
