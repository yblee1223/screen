import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time

# 특정 프로그램 창 이름 (예: 'Untitled - Notepad')
window_title = "Untitled - Notepad"

# 해당 창을 찾기
window = gw.getWindowsWithTitle(window_title)[0]

# 비디오 파일 저장을 위한 코덱 정의 및 VideoWriter 객체 생성
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("window_record.avi", fourcc, 20.0, (window.width, window.height))

# 레코딩 시작
start_time = time.time()
record_seconds = 10  # 녹화할 시간(초)

while True:
    # 창 영역 캡처
    img = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
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
