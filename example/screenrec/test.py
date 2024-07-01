import pyscreenrec
import time
recorder = pyscreenrec.ScreenRecorder()
recorder.start_recording("recording.mp4", 10) 
time.sleep(10)
recorder.stop_recording()