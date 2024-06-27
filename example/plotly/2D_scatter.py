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

def create_graphs(df):
    # 3D 산점도 생성
    fig_3d = go.Figure()
    fig_3d.add_trace(go.Scatter3d(
        x=df['Position_X'],
        y=df['Position_Y'],
        z=df['Position_Z'],
        mode='markers+lines',
        marker=dict(size=3, color='blue', opacity=0.5),
        line=dict(color='blue', width=2),
        name='Trajectory (3D)'
    ))
    fig_3d.update_layout(
        title="3D Position Tracking",
        scene=dict(
            xaxis_title='Position X',
            yaxis_title='Position Y',
            zaxis_title='Position Z',
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=600,
        width=800,
    )

    # 2D X-Y 평면
    fig_xy = go.Figure()
    fig_xy.add_trace(go.Scatter(
        x=df['Position_X'],
        y=df['Position_Y'],
        mode='markers+lines',
        marker=dict(size=6, color='blue', opacity=0.8),
        line=dict(color='blue', width=2),
        name='Trajectory (X-Y)'
    ))
    fig_xy.update_layout(
        title="2D Trajectory in X-Y Plane",
        xaxis_title='Position X',
        yaxis_title='Position Y',
        height=600,
        width=800,
    )

    # 2D Y-Z 평면
    fig_yz = go.Figure()
    fig_yz.add_trace(go.Scatter(
        x=df['Position_Y'],
        y=df['Position_Z'],
        mode='markers+lines',
        marker=dict(size=6, color='green', opacity=0.8),
        line=dict(color='green', width=2),
        name='Trajectory (Y-Z)'
    ))
    fig_yz.update_layout(
        title="2D Trajectory in Y-Z Plane",
        xaxis_title='Position Y',
        yaxis_title='Position Z',
        height=600,
        width=800,
    )

    # 2D X-Z 평면
    fig_xz = go.Figure()
    fig_xz.add_trace(go.Scatter(
        x=df['Position_X'],
        y=df['Position_Z'],
        mode='markers+lines',
        marker=dict(size=6, color='red', opacity=0.8),
        line=dict(color='red', width=2),
        name='Trajectory (X-Z)'
    ))
    fig_xz.update_layout(
        title="2D Trajectory in X-Z Plane",
        xaxis_title='Position X',
        yaxis_title='Position Z',
        height=600,
        width=800,
    )

    return fig_3d, fig_xy, fig_yz, fig_xz

# 플롯 생성 및 출력
fig_3d, fig_xy, fig_yz, fig_xz = create_graphs(df)

# Plotly에서 각 그래프를 개별적으로 표시
fig_3d.show()
fig_xy.show()
fig_yz.show()
fig_xz.show()
