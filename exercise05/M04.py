from timeit import timeit

import numpy as np
import streamlit as st
from numba import jit, prange
from plotly import graph_objects as go


def dft_slow(signal):
    N = len(signal)
    spectrum = np.zeros(N, dtype=np.complex128)

    # C-style loop
    for k in prange(N):  # ty: ignore
        for n in range(N):
            spectrum[k] += signal[n] * np.exp(-1j * k * n * 2 * np.pi / N)
        spectrum[k] = 1 / N * spectrum[k]
    return spectrum


def dft_faster(signal):
    N = len(signal)
    spectrum = np.zeros(N, dtype=np.complex128)
    n = np.arange(N)

    # one vectorized sum per frequency instead of the inner loop
    for k in prange(N):  # ty: ignore
        spectrum[k] = 1 / N * np.sum(signal * np.exp(-1j * k * n * 2 * np.pi / N))
    return spectrum


def dft_matrix(signal):
    N = len(signal)
    n = np.arange(N)
    k = n.reshape(-1, 1)  # column vector: k * n broadcasts to the N x N DFT matrix
    return 1 / N * np.exp(-1j * k * n * 2 * np.pi / N) @ signal.astype(np.complex128)


with st.sidebar:
    dft_method_name = st.selectbox(
        label="DFT method",
        options=[
            "Slow (C-style loops)",
            "Faster (NumPy sum)",
            "Matrix (NumPy broadcasting)",
        ],
        index=2,
    )

    jit_it = st.checkbox("JIT compile DFT functions with Numba", value=True)
    jit_parallel = st.checkbox(
        "Enable parallelization in JIT compilation",
        value=False,
        disabled=not jit_it,
    )

match dft_method_name:
    case "Slow (C-style loops)":
        dft = dft_slow
    case "Faster (NumPy sum)":
        dft = dft_faster
    case "Matrix (NumPy broadcasting)":
        dft = dft_matrix
    case _:
        raise ValueError("Invalid DFT method selected")

if jit_it:
    dft = jit(nopython=True, parallel=jit_parallel)(dft)

t_s = st.number_input(
    label="Sampling period (s)",
    min_value=0.001,
    max_value=2.0,
    value=0.25,
    step=0.01,
)

signals = st.text_area(
    label="Input signals (comma separated values) per line",
    value="1, 0, -1, 0\n1, 0, -1, 0, 1",
    height=200,
)
try:
    signals = [
        np.array([float(x) for x in signal.split(",")])
        for signal in signals.split("\n")
        if signal.strip() != ""
    ]
except ValueError:
    st.error("Please enter numbers separated by commas, one signal per line.")
    st.stop()
# integer sample index times t_s, a float arange can produce one sample too many
times = [np.arange(signal.size) * t_s for signal in signals]

sizes = np.sort(np.linspace(0, 1, len(signals)) * 5 + 5)[::-1]
fig = go.Figure()
for i, (t, signal) in enumerate(zip(times, signals, strict=True)):
    fig.add_trace(
        go.Scatter(
            x=t,
            y=signal,
            mode="markers",
            marker=dict(size=sizes[i]),
            name=f"Signal {i + 1}",
        )
    )
fig.update_layout(
    xaxis=dict(title="Time", ticksuffix="s"),
    yaxis=dict(title="Signal"),
)
st.plotly_chart(fig)

spectra = [dft(signal) for signal in signals]
benchmark = timeit(lambda: [dft(signal) for signal in signals], number=10) / 10
st.write(f"DFT computation time using '{dft_method_name}': {benchmark * 1e3:.3f} ms")
f_s = 1 / t_s
frequencies = [np.arange(spectrum.size) * f_s / spectrum.size for spectrum in spectra]

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
