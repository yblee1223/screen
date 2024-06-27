import plotly.express as px
import plotly.graph_objects as go

def create_animation(df):
    # Create the 3D scatter plot with animation
    fig = px.scatter_3d(df, x='Position_X', y='Position_Y', z='Position_Z',
                        animation_frame='current_time',  # Use 'current_time' for the animation frame
                        range_x=[df['Position_X'].min(), df['Position_X'].max()],
                        range_y=[df['Position_Y'].min(), df['Position_Y'].max()],
                        range_z=[df['Position_Z'].min(), df['Position_Z'].max()],
                        title="3D Position Tracking",
                        opacity=0.8,
                        color='current_time'  # Color by time for better visualization
                       )

    # Add trace for all points
    fig.add_trace(
        go.Scatter3d(
            x=df['Position_X'],
            y=df['Position_Y'],
            z=df['Position_Z'],
            mode='markers+lines',  # Show both markers and lines
            marker=dict(size=3, color='blue', opacity=0.5),
            line=dict(color='blue', width=2),
            name='Full Trajectory'
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
    )
    return fig

# Example usage
# Importing libraries and creating a sample dataframe
import pandas as pd
import numpy as np

# Sample data creation
num_points = 100
df = pd.DataFrame({
    'Position_X': np.cos(np.linspace(0, 2 * np.pi, num_points)),
    'Position_Y': np.sin(np.linspace(0, 2 * np.pi, num_points)),
    'Position_Z': np.linspace(0, 2 * np.pi, num_points),
    'current_time': np.linspace(0, 1, num_points)
})

fig = create_animation(df)
fig.show()
