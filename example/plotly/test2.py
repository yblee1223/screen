import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

# 샘플 데이터 생성
num_points = 100
df = pd.DataFrame({
    'Position_X': np.cos(np.linspace(0, 2 * np.pi, num_points)),
    'Position_Y': np.sin(np.linspace(0, 2 * np.pi, num_points)),
    'Position_Z': np.linspace(0, 2 * np.pi, num_points),
    'current_time': np.linspace(0, 1, num_points)
})

def create_combined_graph(df):
    # 서브플롯 만들기
    fig = make_subplots(
        rows=4, cols=1,
        specs=[[{'type': 'scatter3d'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'scatter'}]],
        subplot_titles=("3D Trajectory", "X-Y Plane", "Y-Z Plane", "X-Z Plane")
    )

    # 3D 산점도 추가
    fig.add_trace(go.Scatter3d(
        x=df['Position_X'],
        y=df['Position_Y'],
        z=df['Position_Z'],
        mode='markers+lines',
        marker=dict(size=1, color='blue', opacity=0.5),
        line=dict(color='blue', width=2),
        name='Trajectory (3D)'
    ), row=1, col=1)

    # 2D X-Y 평면 추가
    fig.add_trace(go.Scatter(
        x=df['Position_X'],
        y=df['Position_Y'],
        mode='markers+lines',
        marker=dict(size=6, color='blue', opacity=0.8),
        line=dict(color='blue', width=2),
        name='Trajectory (X-Y)'
    ), row=2, col=1)

    # 2D Y-Z 평면 추가
    fig.add_trace(go.Scatter(
        x=df['Position_Y'],
        y=df['Position_Z'],
        mode='markers+lines',
        marker=dict(size=6, color='green', opacity=0.8),
        line=dict(color='green', width=2),
        name='Trajectory (Y-Z)'
    ), row=3, col=1)

    # 2D X-Z 평면 추가
    fig.add_trace(go.Scatter(
        x=df['Position_X'],
        y=df['Position_Z'],
        mode='markers+lines',
        marker=dict(size=6, color='red', opacity=0.8),
        line=dict(color='red', width=2),
        name='Trajectory (X-Z)'
    ), row=4, col=1)

    # 레이아웃 업데이트
    fig.update_layout(
        height=900,
        width=1000,
        title_text="3D and 2D Trajectories",
        showlegend=False,  # 범례를 한번만 나타내기 위해 숨김
        scene=dict(
            xaxis_title='Position X',
            yaxis_title='Position Y',
            zaxis_title='Position Z'
        ),
        xaxis=dict(title='Position X'),
        yaxis=dict(title='Position Y'),
        xaxis2=dict(title='Position Y'),
        yaxis2=dict(title='Position Z'),
        xaxis3=dict(title='Position X'),
        yaxis3=dict(title='Position Z'),
        margin=dict(l=0, r=0, t=30, b=0)
    )

    return fig

# 플롯 생성 및 출력
fig = create_combined_graph(df)
fig.show()
