import pyscreenrec
import cv2
recorder = pyscreenrec.ScreenRecorder()

# to start recording
recorder.start_recording("recording.mp4", 10) 
# 'recording.mp4' is the name of the output video file, may also contain full path like 'C:/Users/<user>/Videos/video.mp4'
# the second parameter(10) is the FPS. You can specify the FPS for the screen recording using the second parameter. It must not be greater than 60.

# to pause recording
recorder.pause_recording()

# to resume recording
recorder.resume_recording()

# to stop recording
recorder.stop_recording()