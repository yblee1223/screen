import streamlit as st
# from streamlit_pdf_viewer import pdf_viewer
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lib.data.img import *
from lib.data.text import tutorial_description
from lib.graphic import local_css

def tutorial_video():
    video_file = open('./data/asset/video/tutorial.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)

def side_bar():
    with st.sidebar:
        st.image(wonju_logo, use_column_width=True)
        st.caption(tutorial_description)
        st.write("---")
        st.image(whatslab_logo, use_column_width=False, width=logo_width)
        st.image(almaroco_logo, use_column_width=False, width=logo_width)

if __name__=="__main__":
    st.set_page_config(
        page_title="튜토리얼", 
        page_icon=yensei_icon
    )
    local_css(os.path.join('src','css','style.css'))
    side_bar()
    st.caption("재활마을 둘러보기")
    tutorial_video()
    st.caption("프로그램 사용 매뉴얼")
    pdf_file_name = os.path.join('data','asset','pdf','manual.pdf')
    with open(pdf_file_name, "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="튜토리얼 pdf",
                        data=PDFbyte,
                        file_name='manual.pdf',
                        mime='application/octet-stream')

    # st.write(read_pdf(pdf_file_name))
    # pdf_viewer(os.path.join("data", "asset", "pdf", "manual.pdf"))
    # st.write(read_pdf("data/asset/pdf/manual.pdf"))

