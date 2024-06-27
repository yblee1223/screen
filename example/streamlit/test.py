import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Streamlit Session State",
    page_icon="🧊"
)

# 세션 상태에 기본값을 설정합니다.
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 50

# 슬라이더를 사용하여 세션 상태 값을 업데이트합니다.
num_rows = st.sidebar.slider('Number of rows', min_value=10, max_value=100, value=st.session_state.num_rows)

# 슬라이더 값이 변경될 때마다 세션 상태를 업데이트합니다.
st.session_state.num_rows = num_rows

# 슬라이더 값을 사용하여 DataFrame을 생성합니다.
data = {
    'x': range(st.session_state.num_rows),
    'y': [i ** 2 for i in range(st.session_state.num_rows)]
}
df = pd.DataFrame(data)

# DataFrame을 메인 페이지에 표시합니다.
st.write(df)

# Plotly를 사용하여 그래프를 생성합니다.
fig = px.line(df, x='x', y='y', title='Line Chart of y = x^2')

# 그래프를 메인 페이지에 표시합니다.
st.plotly_chart(fig)
