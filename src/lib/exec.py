import time
import os
import shutil
import subprocess
import json
import pandas as pd
import time
import sys


sys.path.append(os.path.join('.', 'src', 'lib'))

from lib.file import *

recorder = None

def startTest(user_name, content, level, timestr):
    global recorder
    print(f"{user_name}의 테스트를 시작합니다")
    print(f"콘텐츠: {content}")
    print(f"난이도: level{level}")

    # file remove
    if len(os.listdir(os.path.join(".", "data", "dummy"))):
        shutil.rmtree(os.path.join(".", "data", "dummy"))
        os.mkdir(os.path.join(".", "data", "dummy"))
        print("ACTION: Remove dummy file ")

    unity_content = f"{content}_Level{level}.exe" # unity content file name
    file_name = f"{user_name}_{content}_{level}_{timestr}"
    dummy_path = os.path.join(".", "data", "dummy", "tmp")
    unity_path = os.path.join(".", "data", "unity", content, f"{content}_Level{level}")
    
    # unity file copy
    shutil.copytree(unity_path, dummy_path) 

    try:
        # unity file execute
        subprocess.Popen([os.path.join(dummy_path, unity_content)])
    except:
        error_text = "ERROR: 콘텐츠를 재생할 수 없습니다"
        print(error_text)
        return error_text
    
    try:
        recorder = ScreenRecorder()
        recorder.start_recording(file_name)
    except:
        error_text = "ERROR: 영상을 녹화할 수 없습니다."
        print(error_text)
        return error_text

def stopTest(user_name, content, level, timestr):
    global recorder
    file_name = f"{user_name}_{content}_{level}_{timestr}"
    input_path = os.path.join(".", "data", "input")
    dummy_path = os.path.join(".", "data", "dummy", "tmp")

    # program kill
    try:
        unity_content = f"{content}_Level{level}.exe"
        os.system(f"taskkill /im {unity_content}")
    except:
        error_text = "ERROR: 프로그램을 종료할 수 없습니다."
        print(error_text)
        return error_text
    
    try:
       recorder.stop_recording()
    except:
        error_text = "ERROR: 영상을 저장할 수 없습니다."
        print(error_text)
        return error_text

    # file save
    try:
        df = json2csv(os.path.join(dummy_path, f"{content}_Level{level}_Data", "data.json"))
        df.to_csv(os.path.join(input_path, f"{file_name}.csv"), index=False)
    except:
        error_text = "ERROR: 데이터가 생성되지 않았습니다."
        print(error_text)
        return error_text
    
    # file remove
    try:
        time.sleep(10)
        shutil.rmtree(os.path.join(".", "data", "dummy"))
        os.mkdir(os.path.join(".", "data", "dummy"))
    except:
        error_text = "ERROR: 파일을 찾을 수 없습니다."
        print(error_text)
        return error_text

    return False

def json2csv(file_name):
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    user_name = "홍길동"
    content = "BalanceBall"
    level = 1
    timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    startTest(user_name, content, level, timestr)
    time.sleep(20)
    stopTest(user_name, content, level, timestr)