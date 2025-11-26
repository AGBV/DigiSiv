import numpy as np
import streamlit as st
from plotly import graph_objects as go


def dft(signal):
    N = len(signal)
    spectrum = np.zeros(N, dtype=complex)

    # C style version
    for k in range(N):
        for n in range(N):
            spectrum[k] = spectrum[k] + signal[n] * np.exp(-1j * k * n * 2 * np.pi / N)
        spectrum[k] = 1 / N * spectrum[k]
    return spectrum


t_s = st.number_input(
    label="Sampling period (s)",
    min_value=0.001,
    max_value=2.0,
    value=0.25,
    step=0.01,
)

signals = st.text_area(
    label="Input signals (comma separated values) per line",
    value="1, 0, -1, 0\n1,0,-1,0,1",
    height=100,
)
signals = [
    np.array([float(x) for x in signal.split(",")])
    for signal in signals.split("\n")
    if signal.strip() != ""
]
times = [np.arange(0, signal.size * t_s, t_s) for signal in signals]

fig = go.Figure()
for i, (time, signal) in enumerate(zip(times, signals, strict=True)):
    fig.add_trace(
        go.Scatter(
            x=time,
            y=signal,
            mode="markers",
            marker=dict(size=signal.size),
            name=f"Signal {i + 1}",
        )
    )
fig.update_layout(
    xaxis=dict(title="Time", ticksuffix="s"),
    yaxis=dict(title="Signal"),
)
st.plotly_chart(fig)

spectra = [dft(signal) for signal in signals]
f_s = 1 / t_s
frequencies = [np.arange(0, f_s, f_s / spectrum.size) for spectrum in spectra]

fig = go.Figure()
for i, (frequency, spectrum) in enumerate(zip(frequencies, spectra, strict=True)):
    fig.add_trace(
        go.Scatter(
            x=frequency,
            y=np.abs(spectrum),
            mode="markers",
            name=f"Spectrum {i + 1}",
        )
    )
fig.update_layout(
    xaxis=dict(title="Frequency", ticksuffix="Hz"),
    yaxis=dict(title="Amplitude"),
)
st.plotly_chart(fig)
