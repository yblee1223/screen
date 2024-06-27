import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime
import pandas as pd
import time
import os
import plotly.express as px
from plotly.subplots import make_subplots
import json
from PIL import Image
import shutil

def startTest(user_id, content_select, level):
    if len(user_id) == 0:
        st.error("사용자 이름을 입력해주세요")
        return

    print(f"{user_id}의 테스트를 시작합니다")
    print(f"콘텐츠: {content_select}")
    print(f"난이도: level{level}")
    timestr = time.strftime("%Y%m%d%H%M%S")
    st.session_state.latest_test_time = timestr
    unity_content = f"{content_select}_level{level}.exe"
    user_test_path = os.path.join(".", "datas", "user_test", f"{user_id}_{content_select}_level{level}_{timestr}")
    unity_content_path = os.path.join(".", "datas", "unity_contents",f"{content_select}_level{level}")
    #테스트 폴더 구성
    with st.spinner("테스트를 준비합니다."):
        print(unity_content_path)
        print(user_test_path)
        shutil.copytree(unity_content_path, user_test_path)
        st.session_state.onTest=True
        import subprocess 
        subprocess.Popen([os.path.join(user_test_path,unity_content)])
        time.sleep(10)
    # os.system(os.path.join(user_test_path,unity_content))

    return
def milliseconds_from_timedelta(timedelta):
    """Compute the milliseconds in a timedelta as floating-point number"""
    return timedelta.total_seconds() *1e3
def stopTest(user_id, content_select, level):

    if st.session_state.onTest:    
        user_test_path = os.path.join(".", "datas", "user_test", f"{user_id}_{content_select}_level{level}_{st.session_state.latest_test_time}")
        unity_content = f"{content_select}_level{level}.exe"
        # os.remove(os.path.join(user_test_path,unity_content))
        os.system(f"taskkill /im {unity_content}")

        st.session_state.onTest = False
    else:
        st.error("실행중인 테스트가 없습니다")
    return

def dataReport(user_id, content_select, level):
    if st.session_state.onTest:
        st.error("아직 테스트가 진행중입니다. 종료후 진행해주세요.")
    elif st.session_state.latest_test_time != "" and st.session_state.onTest == False:
        user_test_path = os.path.join(".", "datas", "user_test", f"{user_id}_{content_select}_level{level}_{st.session_state.latest_test_time}")
        try:
            print(os.path.join(user_test_path, f"{content_select}_level{level}_Data","data.json"))
            if os.path.exists(os.path.join(user_test_path, f"{content_select}_level{level}_Data","data.json")):
                df =  pd.read_json(os.path.join(user_test_path, f"{content_select}_level{level}_Data","data.json"))
                start = df["current_time"][0]
                df["event"] = ""
                df["spend_time"] = ""
                score = df["Score"]
                state = df["State"]

                fig = px.line(df, x="current_time", y=["Rotation_X", "Rotation_Y", "Rotation_Z"], markers=True,
                              line_shape="linear", render_mode="svg")
                dmax = df[["Rotation_X", "Rotation_Y", "Rotation_Z"]].values.max()
                dmin = df[["Rotation_X", "Rotation_Y", "Rotation_Z"]].values.min()
                cnt = 0

                start_time = df['current_time'][0]
                for i in range(1, len(score)):
                    if score[i] > score[i - 1]:
                        cnt += 1
                        fail_time = df["current_time"][i]
                        df["event"][i] = "Success"
                        df["spend_time"][i] = f"{milliseconds_from_timedelta(fail_time - start_time)}ms"
                        start_time = fail_time

                        fig.add_trace(go.Scatter(x=[df.iloc[i]["current_time"], df.iloc[i]["current_time"]],
                                                 y=[dmin, dmax],
                                                 mode='lines',
                                                 line=dict(color='green', width=2, dash='dash'),
                                                 name=f"{cnt}번째 성공"
                                                 ))
                    if state[i] < state[i - 1]:
                        fail_time = df["current_time"][i]
                        df["event"][i] = "Fail"

                        df["spend_time"][i] = f"{milliseconds_from_timedelta(fail_time - start_time)}ms"
                        start_time = fail_time

                        fig.add_trace(go.Scatter(x=[df.iloc[i]["current_time"], df.iloc[i]["current_time"]],
                                                 y=[dmin, dmax],
                                                 mode='lines',
                                                 line=dict(color='yellow', width=2, dash='dash'),
                                                 name=f"실패"
                                                 ))
                st.plotly_chart(fig)
            else:
                st.error("데이터가 존재하지 않습니다")
        except:
            st.error("JSON 파일이 옳바르지 않습니다")

        st.markdown(f"## 최종 점수: {df.iloc[-1]['Score']}")
        time_spent = df.iloc[-1]['current_time'] - df.iloc[0]['current_time']
        st.markdown(f"## 총 소요시간: {time_spent.total_seconds()}초")

        try:
            os.makedirs(os.path.join("user_result",f"{user_id}_{content_select}_level{level}_{st.session_state.latest_test_time}"), exist_ok=True)
            df.to_csv(os.path.join("user_result",f"{user_id}_{content_select}_level{level}_{st.session_state.latest_test_time}","result.csv"))
            csv_f = open(os.path.join("user_result",f"{user_id}_{content_select}_level{level}_{st.session_state.latest_test_time}","result.csv"), "r")
        except:
            st.error("File handling error")
        for i in range(0, len(score)):
            df["current_time"][i] = f'{str((df["current_time"][i] - start).total_seconds())}초'
        st.dataframe(df)
        st.download_button("CSV 파일 다운로드", data = csv_f, file_name = f"{user_id}_{content_select}_level{level}_{st.session_state.latest_test_time}.csv")
            
    else:
        st.error("아직 테스트를 시행하지않았습니다.")
    return

def tutorial():
    video_file = open('./src/tutorial.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)

def main():
    if 'onTest' not in st.session_state:
        st.session_state.onTest = False
    if 'latest_test_time' not in st.session_state:
        st.session_state.latest_test_time =""
    
    wonju_logo = Image.open('src/wonju_logo.png')
    almaroco_logo = Image.open('src/almaroco_logo.png')
    whatslab_logo = Image.open('src/whatslab_logo.png')

    with st.sidebar:
        st.image(wonju_logo)

        tutorial_button = st.button('재활마을 둘러보기', on_click=tutorial)
        user_id = st.text_input("사용자 이름을 입력하세요", placeholder ="심동현")
        content_select = st.selectbox('콘텐츠 선택',
                                    ['Balanceball'])
        level = st.slider('난이도', 1, 3, 1)

        startTest_button = st.button('검사 시작', on_click = startTest, args=(user_id, content_select, level))
        stopTest_button = st.button('검사 종료', on_click =stopTest, args=(user_id, content_select, level))
        dataReport_button = st.button('결과 분석', on_click =dataReport, args=(user_id, content_select, level))
        st.image(whatslab_logo)
        st.image(almaroco_logo)


if __name__ == "__main__":
    def local_css(file_name):
        with open(file_name, encoding = "utf8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    local_css("style.css")
    main()