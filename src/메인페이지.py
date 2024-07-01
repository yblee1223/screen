import streamlit as st

import pandas as pd
import numpy as np
import datetime
import os
import time
import json

import plotly.express as px
import plotly.graph_objects as go

from lib.data.img import *
from lib.data.text import *
from lib.exec import *
from lib.analysis import *
from lib.file import *
from lib.graphic import report, local_css

def main_page():
    st.write("# 사용자 결과 리포트")
    if st.session_state.on_test:
        print("----------------------- main")
        file_name = lastest_file()
        if not file_name:
            st.error('ERROR: 파일이 존재하지 않습니다.')
            return
        report(file_name)
        
    else:
        st.error("검사를 아직 진행하지 않았습니다.")

def side_bar():
    with st.sidebar:
        st.image(wonju_logo, use_column_width=True)
        user_name = st.text_input("환자 이름 입력", value="홍길동")

        content_kr = st.selectbox('콘텐츠 선택', ['밸런스볼 (BalanceBall)', '피트박스 (FitBox)', '테니스볼 (TennisBall)'])
        level = st.slider('난이도 선택', 1, 3, 1)

        if content_kr == '밸런스볼 (BalanceBall)':
            content = "BalanceBall"
            st.caption(balanceball_description)
        elif content_kr == '피트박스 (FitBox)':
            content = "FitBox"
            st.caption(fitbox_description)
        elif content_kr == '테니스볼 (TennisBall)':
            content = "TennisBall"
            st.caption(tennisball_description)           

        st.markdown("---")

        startTest_button = st.button('검사 시작')
        if user_name:
            if startTest_button: 
                print("----------------------- start")
                timestr = time.strftime("%Y%m%d%H%M%S")
                st.session_state.timestr = timestr
                st.session_state.on_test = False
                st.session_state.user_name = user_name
                st.session_state.content = content
                st.session_state.level = level

                message = startTest(st.session_state.user_name, st.session_state.content, st.session_state.level, st.session_state.timestr)
                if message: st.error(message)
                else: st.success("검사가 시작되었습니다.")

            stopTest_button = st.button('검사 종료')
            if stopTest_button:
                print("----------------------- stop")
                message = stopTest(st.session_state.user_name, st.session_state.content, st.session_state.level, st.session_state.timestr)
                if message: st.error(message)
                else: st.success("검사가 종료되었습니다.")

            dataReport_button = st.button('결과 분석')
            if dataReport_button:
                print("----------------------- report")

                st.session_state.on_test = True
                st.success("분석완료")
        else:
            st.error('환자의 이름을 입력해주세요')


        st.markdown("---")

def logo():
    with st.sidebar:
        st.image(whatslab_logo, use_column_width=False, width=logo_width)
        st.image(almaroco_logo, use_column_width=False, width=logo_width)

def session_init():
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "홍길동"
    if 'content' not in st.session_state:
        st.session_state.content = "BalanceBall"
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'timestr' not in st.session_state:
        st.session_state.timestr = None
    if 'on_test' not in st.session_state:
        st.session_state.on_test = False

def main():
    st.set_page_config(
        page_title="메인페이지", 
        page_icon=yensei_icon
    )
    local_css(os.path.join('src','css','style.css'))
    session_init() # session_state init
    side_bar() # sidebar & setting window
    logo() # logo water mark
    main_page() # main page report



if __name__=="__main__":
    main()