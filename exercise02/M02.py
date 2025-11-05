import numpy as np
import streamlit as st
from plotly import graph_objects as go

sampling_frequency = st.slider("Sampling Frequency", 10.0, 5000.0, 2000.0, 10.0)
start_time = st.slider("Start Time", 0.0, 10.0, 0.0, 0.1)
stop_time = st.slider("Stop Time", 0.1, 10.0, 5.0, 0.1)

time = np.arange(start_time, stop_time, 1 / sampling_frequency)
# or
# number_sampling_points = sampling_frequency * (stop_time - start_time)
# time = np.linspace(start_time, stop_time, number_sampling_points)

subsampling_factor = 10
subsampling_frequancy = sampling_frequency / subsampling_factor

# amplitude = np.array([1, 1.2, 0.6])
col1, col2, col3 = st.columns(3)
with col1:
    amplitude = np.array(
        [
            st.slider("Amplitude 1", 0.0, 2.0, 1.0, 0.1),
            st.slider("Amplitude 2", 0.0, 2.0, 1.2, 0.1),
            st.slider("Amplitude 3", 0.0, 2.0, 0.6, 0.1),
        ]
    )
with col2:
    freq = np.array(
        [
            st.slider("Frequency 1", 0.0, 100.0, 1.0, 1.0),
            st.slider("Frequency 2", 0.0, 100.0, 12.0, 1.0),
            st.slider("Frequency 3", 0.0, 100.0, 45.0, 1.0),
        ]
    )
with col3:
    phases = [np.pi * x for x in [0, 1 / 6, 1 / 4, 1 / 3, 1 / 2, 1]]
    format_func = lambda x: rf"pi/{(x / np.pi) ** -1 if x > 0 else 0}"
    end = len(phases) - 1
    phase = np.array(
        [
            st.selectbox("Phase 1", phases, format_func=format_func, index=0),
            st.selectbox("Phase 2", phases, format_func=format_func, index=end),
            st.selectbox("Phase 3", phases, format_func=format_func, index=4),
            # st.slider("Phase 2", 0.0, 2 * np.pi, 3 * np.pi, 0.1),
            # st.slider("Phase 3", 0.0, 2 * np.pi, np.pi / 2, 0.1),
        ]
    )
signal = np.sum(
    [
        amplitude * np.sin(2 * np.pi * f * time + phase)
        for amplitude, f, phase in zip(amplitude, freq, phase, strict=True)
    ],
    axis=0,
)
#     np.sin(2 * np.pi * time)
#     + 1.2 * np.sin(2 * np.pi * 12 * time + 3 * np.pi)
#     + 0.6 * np.cos(2 * np.pi * 45 * time)

# st.latex(rf"\sin(2\pi{1}) + 1.2 \cdot \sin(2\pi{})")

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=time,
        y=signal,
    )
)
st.plotly_chart(fig)
