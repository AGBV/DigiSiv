import numpy as np
import numpy.typing as npt
import streamlit as st
from plotly import graph_objects as go
from scipy.fft import fft, fftfreq


def sample(
    signal: npt.NDArray,
    sampling_frequency: float,
    new_sampling_frequency: float,
    # hold: bool = False,
):
    if new_sampling_frequency > sampling_frequency:
        raise Exception("The new sampling frequency can't be larger than the old one!")

    sampling_step = int(sampling_frequency // new_sampling_frequency)
    return signal[::sampling_step]


col1, col2, col3, col4 = st.columns(4)
sampling_frequency = col1.number_input("Sampling Frequency", 10.0, 5000.0, 2000.0, 10.0)
start_time = col2.number_input("Start Time", 0.0, 9.0, 0.0, 1.0)
end_time = col3.number_input("Stop Time", 0.001, 10.0, 5.0, 1.0)
subsampling_factor = col4.number_input("Sub-Sampling Factor", 1, 1000, 10, 1)
if start_time >= end_time:
    st.error("Start time has to be lower than end time")
    st.stop()
st.divider()

time = np.arange(start_time, end_time, 1 / sampling_frequency)
# or
# number_sampling_points = sampling_frequency * (end_time - start_time)
# time = np.linspace(start_time, end_time, number_sampling_points)

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

    def format_func(x):
        return f"pi/{(x / np.pi) ** -1 if x > 0 else 0}"

    end = len(phases) - 1
    phase = np.array(
        [
            st.selectbox("Phase 1", phases, format_func=format_func, index=0),
            st.selectbox("Phase 2", phases, format_func=format_func, index=end),
            st.selectbox("Phase 3", phases, format_func=format_func, index=4),
        ]
    )
signal = np.sum(
    [
        amplitude * np.sin(2 * np.pi * f * time + phase)
        for amplitude, f, phase in zip(amplitude, freq, phase, strict=True)
    ],
    axis=0,
)

subsampling_frequancy = sampling_frequency / subsampling_factor
sampled_signal = sample(signal, sampling_frequency, subsampling_frequancy)
sampled_time = np.linspace(start_time, end_time, sampled_signal.size)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=sampled_time,
        y=sampled_signal,
        name="Sampled",
    )
)
fig.add_trace(
    go.Scatter(
        x=time,
        y=signal,
        name="Original",
        line=dict(color="rgba(255, 0, 0, 0.25)"),
    )
)
fig.update_layout(
    title="Signal",
    xaxis=dict(title="Time", ticksuffix="s"),
    yaxis=dict(title="Signal"),
)
st.plotly_chart(fig)

st.divider()
st.info("Extra! See what happens when the sub-sampling factor goes beyond 20 ;)")

spectrum = np.array(fft(signal)) / sampling_frequency
frequency = fftfreq(spectrum.size, 1 / sampling_frequency)
spectrum_sampled = np.array(fft(sampled_signal)) / subsampling_frequancy
frequency_sampled = fftfreq(spectrum_sampled.size, 1 / subsampling_frequancy)

col1, col2 = st.columns(2)
half = col1.checkbox("Show positive spectrum only", value=True)
cutoff_frequency = col2.number_input(
    "Cutoff Frequency",
    0.0,
    float(sampling_frequency / 2),
    float(sampling_frequency / 2),
    1.0,
)
if half:
    spectrum = spectrum[0 : len(spectrum) // 2]
    frequency = frequency[0 : len(frequency) // 2]
    spectrum_sampled = spectrum_sampled[0 : len(spectrum_sampled) // 2]
    frequency_sampled = frequency_sampled[0 : len(frequency_sampled) // 2]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=frequency_sampled,
        y=np.abs(spectrum_sampled),
        name="Sampled",
    )
)
fig.add_trace(
    go.Scatter(
        x=frequency,
        y=np.abs(spectrum),
        name="Original",
        line=dict(color="rgba(255, 0, 0, 0.5)"),
    )
)
fig.update_layout(
    title="Spectrum",
    xaxis=dict(title="Frequency", ticksuffix="Hz", range=[0, cutoff_frequency]),
    yaxis=dict(title="Spectrum"),
)
st.plotly_chart(fig)
