import os
import pandas as pd
import streamlit as st
import sys

import plotly.express as px
import plotly.graph_objects as go


sys.path.append(os.path.join('.', 'src', 'lib'))

from lib.analysis import *

def print_profile(file_name, score, time_spent, fps):
    user_name, content, level, timestr = file_name.split('_')
    timestr = timestr.split('.')[0]
    text = f'''
            ```json
            "사용자 이름" : {user_name}
            "콘텐트 이름" : {content}
            "난이도" : {level}
            "파일 번호" : {timestr}
            "점수" : {score}
            "운동시간 (초)" : {round(time_spent, 2)}
            "정보량 (fps)" : {round(fps, 2)}
            ```
            '''
    return text

def report(file_name):
    input_path = os.path.join('.', 'data', 'input')
    output_path = os.path.join('.', 'data', 'output')

    if file_name in os.listdir(output_path):
        df = pd.read_csv(os.path.join(output_path, file_name))
        # st.caption('[output 저장소]')
    else:
        df = pd.read_csv(os.path.join(input_path, file_name))
        df = preprocessing(df)
        # st.caption('[input 저장소]')
        if 'TennisBall' in file_name:
            df = position_extract(df)
            df = pose_scailing(df)
    
    score = score_report(df)
    time_spent = time_report(df)
    fps = df.shape[0] / time_spent

    st.caption('환자 프로필')
    st.markdown(print_profile(file_name, score, time_spent, fps))
    st.markdown('')

    st.caption('운동 영상')
    file_path = file_name.split('.')[0]
    video_file = open(os.path.join('data', 'video', f'{file_path}.mp4'), 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.caption('환자 HMD 데이터 분석 그래프 Rotation')
    st.plotly_chart(rotation_graph(df))

    if 'TennisBall' in file_name:
        st.caption('환자 컨트롤러 데이터 분석 그래프 Position')
        st.plotly_chart(position_graph_1(df))
        if st.checkbox('정규화된 position 데이터 보기'):
            st.caption('환자 컨트롤러 데이터 분석 그래프 Position (scaled)')
            st.plotly_chart(position_graph_2(df))  
        
        if st.checkbox("위치 정보 애니메이션 생성"):
            st.plotly_chart(create_animation(df, int(fps)))
    
    st.caption('환자 데이터 파일')
    df = sort_columns_alphabetically(df)
    st.dataframe(df)

    try:
        df.to_csv(os.path.join(output_path, file_name), header=True, index=None)
    except:
        st.error("ERROR: 중복된 파일 참조입니다.")
    csv_f = open(os.path.join("data", "output", file_name,), "r")
    st.download_button("CSV 파일 다운로드", data = csv_f, file_name = file_name)

def position_graph_1(df):
    fig = px.line(df, x="current_time", y=["Position_X", "Position_Y", "Position_Z"], markers=False,
                  line_shape="linear", render_mode="svg")
    fig = draw_event(df, fig, ["Position_X", "Position_Y", "Position_Z"])
    return fig

def position_graph_2(df):
    fig = px.line(df, x="current_time", y=['Scaled_Position_X', 'Scaled_Position_Y', 'Scaled_Position_Z'], markers=False,
                  line_shape="linear", render_mode="svg")
    fig = draw_event(df, fig, ['Scaled_Position_X', 'Scaled_Position_Y', 'Scaled_Position_Z'])
    return fig

def rotation_graph(df):
    fig = px.line(df, x="current_time", y=["Rotation_X","Rotation_Y","Rotation_Z"], markers=False,
            line_shape="linear", render_mode="svg")
    fig = draw_event(df, fig, ["Rotation_X", "Rotation_Y", "Rotation_Z"])
    return fig

def draw_event(df, fig, columns):
    score = df["Score"]
    dmax = df[columns].values.max()
    dmin = df[columns].values.min()
    cnt = 0

    for i in range(1, len(score)):
        if df["event"][i] == "Success":
            cnt += 1
            fig.add_trace(go.Scatter(x=[df.iloc[i]["current_time"], df.iloc[i]["current_time"]],
                                        y=[dmin, dmax],
                                        mode='lines',
                                        line=dict(color='green', width=2, dash='dash'),
                                        name=f"{cnt}번째 성공"
                                        ))
        if df["event"][i] == "Fail":
            fig.add_trace(go.Scatter(x=[df.iloc[i]["current_time"], df.iloc[i]["current_time"]],
                                        y=[dmin, dmax],
                                        mode='lines',
                                        line=dict(color='yellow', width=2, dash='dash'),
                                        name=f"실패"
                                        ))
    return fig


def create_animation(df, default=60):
    # Group data into 30 fps intervals
    df = df.copy()
    max = df.shape[0]
    if max < default:
        default = max
    gap = st.slider(
        "fps 설정 (기본값: 1초에 재생되는 모든 프레임)",
        1, max, default)
    df['frame'] = (df.index // gap).astype(int)
    
    fig = px.scatter_3d(df, x='Position_X', y='Position_Y', z='Position_Z',
                        animation_frame='frame',  
                        range_x=[df['Position_X'].min(), df['Position_X'].max()],
                        range_y=[df['Position_Y'].min(), df['Position_Y'].max()],
                        range_z=[df['Position_Z'].min(), df['Position_Z'].max()],
                        title="3D Position Tracking",
                        opacity=0.8,
                       )
    
    fig.add_trace(
        go.Scatter3d(
            x=df['Position_X'],
            y=df['Position_Y'],
            z=df['Position_Z'],
            mode='lines',  
            line=dict(color='black', width=2),
            name='전체 궤적'
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis_title='Position X',
            yaxis_title='Position Y',
            zaxis_title='Position Z',
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=600,
        width=800,
        sliders=[{
            'steps': [{
                'args': [[f.name], {'frame': {'duration': 10, 'redraw': True}, 'mode': 'immediate'}],
                'label': f.name,
                'method': 'animate',
            } for f in fig.frames],
            'transition': {'duration': 0},
        }],
        
        updatemenus=[{
            'buttons': [{
                'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],
                'label': '재생',
                'method': 'animate',
            }, {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                'label': '정지',
                'method': 'animate',
            }],
            'showactive': True,
            'type': 'buttons',
        }]
    )
    
    fig.update_traces(marker=dict(
        size=3,
        color='blue', 
        opacity=0.6,   
        symbol='circle',  
    ))
    
    df = df.drop(['frame'], axis=1)

    return fig


def local_css(file_name):
    with open(file_name, encoding = "utf8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if __name__ == "__main__":
    print(sys.path)