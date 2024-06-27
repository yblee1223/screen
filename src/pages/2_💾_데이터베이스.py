import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lib.data.img import *
from lib.data.text import database_description
from lib.graphic import report, local_css

def main_page():
    file_name = st.selectbox('선택', options=st.session_state.search_dir)
    if file_name == None:
        st.error('ERROR: 파일이 존재하지 않습니다.')
        return
    report(file_name)
    
def side_bar():
    with st.sidebar:
        st.image(wonju_logo, use_column_width=True)
        st.caption(database_description)
        st.write("---")
        user_name = st.text_input("환자 이름 입력", value="")
        content_kr = st.selectbox('콘텐츠 선택', ['밸런스볼 (BalanceBall)', '피트박스 (FitBox)', '테니스볼 (TennisBall)'])

        if content_kr == '밸런스볼 (BalanceBall)':
            content = "BalanceBall"
        elif content_kr == '피트박스 (FitBox)':
            content = "FitBox"
        elif content_kr == '테니스볼 (TennisBall)':
            content = "TennisBall"

        input_path = os.path.join('.', 'data', 'input')
        dir = os.listdir(input_path)
        # if dir == None:
        #     st.session_state.search_dir = []
        # else:
        st.session_state.search_dir = [file for file in dir if (content in file) and (user_name in file)]

        st.markdown("---")

        st.image(whatslab_logo, use_column_width=False, width=logo_width)
        st.image(almaroco_logo, use_column_width=False, width=logo_width)

def main():
    st.set_page_config(
        page_title="데이터베이스", 
        page_icon=yensei_icon
    )
    local_css(os.path.join('src','css','style.css'))
    side_bar()
    main_page()

def session_init():
    if 'search_dir' not in st.session_state:
        st.session_state.search_dir = []

if __name__=="__main__":
    main()