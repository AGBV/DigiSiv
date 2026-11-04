from pathlib import Path

import numpy as np
import streamlit as st
from plotly import graph_objects as go
from scipy.fft import fft, fftfreq
from scipy.io import wavfile
from scipy.signal import find_peaks

audio_file = st.file_uploader("Choose an audio file", type=["wav"])
if audio_file is None:
    audio_file = Path(__file__).parent / "audio01.wav"
    st.info("Using default audio file")

sampling_rate, audio_signal = wavfile.read(audio_file)
if np.issubdtype(audio_signal.dtype, np.integer):  # e.g. int16 -> [-1, 1)
    audio_signal = audio_signal / (np.iinfo(audio_signal.dtype).max + 1)
if audio_signal.ndim > 1:  # stereo -> mono
    audio_signal = audio_signal.mean(axis=1)
st.audio(audio_signal, sample_rate=sampling_rate)

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
segment = audio_signal[int(start_t * sampling_rate) : int(end_t * sampling_rate)]
sampled_time = start_t + np.arange(segment.size) / sampling_rate

fig = go.Figure()
fig.add_trace(go.Scatter(x=sampled_time, y=segment))
fig.update_layout(
    xaxis=dict(
        title="Time",
        ticksuffix="s",
    ),
    yaxis=dict(title="Signal"),
)
st.plotly_chart(fig)

# spectrum of the selected segment, frequency resolution 1 / segment length
spectrum = np.asarray(fft(segment)) / segment.size
frequency = fftfreq(segment.size, 1 / sampling_rate)
st.caption(
    f"Spectrum of the selected {segment.size / sampling_rate:g} s, "
    f"frequency resolution {sampling_rate / segment.size:g} Hz. "
    "Try a segment length that is not a whole number of seconds to see leakage."
)

half = st.checkbox("Show one-sided spectrum only", value=True)
if half:
    # positive frequencies, doubled to account for the negative ones (except DC)
    spectrum = 2 * spectrum[: spectrum.size // 2]
    spectrum[0] /= 2
    frequency = frequency[: frequency.size // 2]

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

if half:
    amplitude = np.abs(spectrum)
    peaks, _ = find_peaks(amplitude, height=0.05 * amplitude.max())
    peaks = peaks[np.argsort(amplitude[peaks])[::-1][:20]]
    st.subheader(f"Strongest frequencies ({peaks.size})")
    st.dataframe(
        {
            "Frequency (Hz)": frequency[np.sort(peaks)],
            "Amplitude": amplitude[np.sort(peaks)],
        },
        hide_index=True,
    )
