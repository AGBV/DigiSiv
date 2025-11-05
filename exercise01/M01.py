from pathlib import Path

import numpy as np
import streamlit as st
from plotly import graph_objects as go
from scipy.fft import fft, fftfreq, fftshift
from scipy.io import wavfile

audio_file = st.file_uploader("Choose an audio file", type=["wav"])
if audio_file is None:
    audio_file = Path(__file__).parent / "audio01.wav"
    st.info("Using default audio file")

sampling_rate, audio_signal = wavfile.read(audio_file)
audio_signal = audio_signal * pow(2, -15)

start_t = st.number_input(
    "Start time (s)",
    min_value=0.0,
    max_value=float(len(audio_signal) / sampling_rate),
    value=0.0,
    step=0.1,
)
end_t = st.number_input(
    "End time (s)",
    min_value=0.0,
    max_value=float(len(audio_signal) / sampling_rate),
    value=1.0,
    step=0.1,
)
if end_t <= start_t:
    st.error("Make sure that the end time is greater than the start time.")
    st.stop()
sampled_time = np.arange(start_t, end_t, 1 / sampling_rate)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=sampled_time,
        y=audio_signal[
            np.int64(start_t * sampling_rate) : np.int64(end_t * sampling_rate)
        ],
    )
)
fig.update_layout(
    xaxis=dict(
        title="Time",
        ticksuffix="s",
    ),
    yaxis=dict(title="Signal"),
)
st.plotly_chart(fig)

spectrum = fft(audio_signal[0:sampling_rate]) / sampling_rate
frequency = fftfreq(len(spectrum), 1 / sampling_rate)

half = st.checkbox("Show half spectrum only", value=True)
if half:
    spectrum = spectrum[0 : len(spectrum) // 2]
    frequency = frequency[0 : len(frequency) // 2]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=frequency,
        y=np.abs(spectrum),
    )
)
fig.update_layout(
    xaxis=dict(
        title="Frequency",
        ticksuffix="Hz",
    ),
    yaxis=dict(title="Amplitude"),
)
st.plotly_chart(fig)
