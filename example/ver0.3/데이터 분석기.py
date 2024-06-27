import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pandas as pd
import time
import os
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
from PIL import Image
import numpy as np
import shutil

def startSearch(user_id):
    if user_id == "":
        st.error("환자의 이름을 입력해주세요")
        return
    test_path = os.path.join(".","datas","user_test")
    test_name_list = os.listdir(test_path)
    user_test_list = [test for test in test_name_list if user_id in test]
    if not user_test_list:
        st.error("입력하신 환자의 데이터가 없습니다")
        return
    st.session_state.user_test_list = user_test_list
    return

def milliseconds_from_timedelta(timedelta):
    """Compute the milliseconds in a timedelta as floating-point number"""
    return timedelta.total_seconds() *1e3

def dataReport(user_info):
    _,content_select,level,_ = user_info.split("_")
    user_test_path = os.path.join(".", "datas", "user_test", f"{user_info}")

    if os.path.exists(os.path.join(user_test_path, f"{content_select}_{level}_Data","data.json")):
        df =  pd.read_json(os.path.join(user_test_path, f"{content_select}_{level}_Data","data.json"))

        start = df["current_time"][0]
        df["event"] = ""
        df["spend_time"] = ""
        score = df["Score"]
        state = df["State"]


        fig = px.line(df, x="current_time", y=["Rotation_X","Rotation_Y","Rotation_Z"], markers=True,
            line_shape="linear", render_mode="svg")
        dmax = df[["Rotation_X","Rotation_Y","Rotation_Z"]].values.max()
        dmin = df[["Rotation_X","Rotation_Y","Rotation_Z"]].values.min()
        cnt = 0

        start_time = df['current_time'][0]
        for i in range(1,len(score)):
            if score[i] > score[i-1]:
                cnt += 1
                
                fail_time = df["current_time"][i]
                df["event"][i] = "Success"
                df["spend_time"][i] = f"{milliseconds_from_timedelta(fail_time - start_time)}ms"
                start_time = fail_time

                fig.add_trace(go.Scatter(x=[df.iloc[i]["current_time"],df.iloc[i]["current_time"]],
                        y=[dmin,dmax],
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
    st.markdown(f"## 최종 점수: {df.iloc[-1]['Score']}")

    time_spent = df.iloc[-1]['current_time'] - df.iloc[0]['current_time']

    st.markdown(f"## 총 소요시간: {time_spent.total_seconds()}초")


    try:
        os.makedirs(os.path.join("user_result",f"{user_info}"), exist_ok=True)
        df.to_csv(os.path.join("user_result",f"{user_info}","result.csv"))
        csv_f = open(os.path.join("user_result",f"{user_info}","result.csv"), "r")
    except:
        st.error("File handling error")

    for i in range(0, len(score)):
        df["current_time"][i] = f'{str((df["current_time"][i] - start).total_seconds())}초'


    st.write(df)
    st.download_button("CSV 파일 다운로드", data = csv_f, file_name = f"{user_info}.csv")

    return

def main():
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ''
    if 'user_test_list' not in st.session_state:
        st.session_state.user_test_list = []

    wonju_logo = Image.open('src/wonju_logo.png')
    almaroco_logo = Image.open('src/almaroco_logo.png')
    whatslab_logo = Image.open('src/whatslab_logo.png')

    with st.sidebar:
        st.image(wonju_logo)
        user_id = st.text_input("검색할 환자의 이름을 입력하세요", placeholder ="심동현")
        searchButton = st.button("찾기", on_click = startSearch, args=(user_id,))
        # 빈 공간 추가
        empty_block = st.empty()
        empty_block.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
        # st.markdown("<br style='line-height:500px;'>", unsafe_allow_html=True) 
        st.image(whatslab_logo, use_column_width=True)
        st.image(almaroco_logo, use_column_width=True)


        
    user_info = st.selectbox('환자 선택',options = st.session_state.user_test_list)
    st.button("결과 분석", on_click = dataReport, args=(user_info,))

    
if __name__ == "__main__":
    def local_css(file_name):
        with open(file_name, encoding = "utf8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    local_css("style.css")
    main()