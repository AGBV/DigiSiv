import io
from pathlib import Path

import numpy as np
import scipy.signal as signal
import streamlit as st
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from scipy.io import wavfile

# --- HILFSFUNKTIONEN ---


def generate_synthetic_signal(fs=44100, duration=2.0):
    """Erzeugt ein Fallback-Signal, falls keine Datei vorhanden ist."""
    t = np.arange(0, duration, 1 / fs)
    # Ein Mix aus Frequenzen
    sig = (
        0.5 * np.cos(2 * np.pi * 440 * t)
        + 0.3 * np.cos(2 * np.pi * 880 * t)
        + 0.2 * np.random.normal(0, 0.1, len(t))
    )  # Mit etwas Rauschen
    return fs, sig


def load_and_normalize_audio(file_or_path):
    """Lädt Audio, konvertiert zu Mono und normalisiert auf Float [-1, 1]."""
    try:
        fs, data = wavfile.read(file_or_path)

        # Stereo zu Mono
        if data.ndim > 1:
            data = data.mean(axis=1)

        # Normalisierung (Int zu Float)
        data = data.astype(np.float32)
        max_val = np.max(np.abs(data))
        if max_val > 0:
            data /= max_val

        return fs, data
    except FileNotFoundError:
        return None, None


@st.cache_data
def calculate_fft(signal_data, fs):
    """Berechnet die FFT (gecached für Performance)."""
    N = len(signal_data)
    # Nur positive Frequenzen (rfft)
    fft_y = np.abs(np.fft.rfft(signal_data)) / N
    fft_x = np.fft.rfftfreq(N, d=1 / fs)
    return fft_x, fft_y


# --- MAIN APP ---

st.set_page_config(page_title="Digital Filter Lab", layout="wide")

# 1. AUDIO LADEN
audio_file = st.file_uploader("Wählen Sie eine WAV-Datei", type=["wav"])

if audio_file is not None:
    sampling_rate, audio_signal = load_and_normalize_audio(audio_file)
else:
    # Versuche handel.wav zu laden, sonst Synthetisch
    default_path = Path(__file__).parent / "handel.wav"
    sampling_rate, audio_signal = load_and_normalize_audio(default_path)

if (audio_signal is None) or (sampling_rate is None):
    st.warning("Keine datei gefunden. Nutze synthetisches Signal.")
    sampling_rate, audio_signal = generate_synthetic_signal()

# Zeitvektor erstellen
t = np.arange(audio_signal.size) / sampling_rate


# 2. SIDEBAR & FILTER LOGIK
filter_types = {
    "mittelwert": "Boxcar",
    "polynom": "Savitzky-Golay",
    "normal": "Gauß",
    "median": "Nicht-linear",
    "butterworth": "IIR Tiefpass",
    "sinc": "FIR",
}

with st.sidebar:
    st.header("Einstellungen")
    filter_key = st.selectbox(
        "Filter Typ",
        options=list(filter_types.keys()),
        index=0,
        format_func=lambda x: f"{x.capitalize()} ({filter_types[x]})",
    )

    # Dynamische Slider-Grenzen je nach Audio-Länge sinnvoll, aber 51 ist okay für Demo
    window_len = st.slider(
        "Fensterlänge (Punkte)",
        min_value=3,
        max_value=101,  # Etwas erhöht für hörbare Effekte bei hoher Samplerate
        value=7,
        step=2,
    )

# Filter anwenden
sig_filtered = np.zeros_like(audio_signal)
kernel_viz = None

match filter_key:
    case "mittelwert":
        kernel = np.ones(window_len) / window_len
        sig_filtered = signal.lfilter(kernel, 1, audio_signal)
        # sig_filtered = signal.convolve(audio_signal, kernel, mode="same")
        kernel_viz = kernel
    case "polynom":
        poly_order = 2
        if window_len <= poly_order:
            st.error(f"Fensterlänge muss > {poly_order} sein.")
            st.stop()

        sig_filtered = signal.savgol_filter(
            audio_signal,
            window_length=window_len,
            polyorder=poly_order,
        )

        # Impulsantwort für Visualisierung rekonstruieren
        impulse = np.zeros(window_len * 2)
        impulse[window_len] = 1.0
        kernel_viz = signal.savgol_filter(impulse, window_len, poly_order)
        # Slicing um das Zentrum
        mid = window_len
        kernel_viz = kernel_viz[mid - window_len // 2 : mid + window_len // 2 + 1]

    case "normal":
        sigma = st.sidebar.number_input(
            "Sigma (σ)", min_value=0.1, max_value=20.0, value=2.0, step=0.1
        )
        # Gauß Kernel
        kernel = signal.windows.gaussian(window_len, std=sigma)  # pyright: ignore
        kernel /= np.sum(kernel)
        sig_filtered = signal.lfilter(kernel, 1, audio_signal)
        kernel_viz = kernel
    case "median":
        # Fensterlänge muss ungerade sein
        if window_len % 2 == 0:
            window_len += 1

        sig_filtered = signal.medfilt(audio_signal, kernel_size=window_len)

        # Median hat keine klassische "Impulsantwort" im linearen Sinne,
        # aber wir können zeigen, was er aus einem Impuls macht (nämlich nichts, wenn er schmal ist!)
        # Visualisierung: Wir nehmen eine Rampe mit einem Ausreißer
        viz_len = window_len * 3
        kernel_viz = np.zeros(viz_len)
        # Erzeuge eine Rampe
        kernel_viz = np.linspace(0, 1, viz_len)
        # Füge einen Ausreißer (Knackser) in die Mitte
        kernel_viz[viz_len // 2] = 0.0
        # Filtere die Visualisierung
        kernel_viz = signal.medfilt(kernel_viz, window_len)
    case "butterworth":
        st.sidebar.markdown("---")
        # Cutoff Frequenz statt Fensterlänge
        cutoff = st.sidebar.slider(
            "Grenzfrequenz (Hz)",
            min_value=50,
            max_value=int(sampling_rate / 2) - 1,
            value=1000,
        )
        order = st.sidebar.slider(
            "Ordnung (Steilheit)",
            min_value=1,
            max_value=10,
            value=4,
        )

        # Design des Filters
        sos = signal.butter(order, cutoff, btype="low", fs=sampling_rate, output="sos")
        sig_filtered = signal.sosfiltfilt(
            sos, audio_signal
        )  # sosfiltfilt filtert vor & zurück -> null Phasenverschiebung

        # Impulsantwort für Visualisierung
        # Wir schicken einen Impuls durch
        impulse = np.zeros(100)  # Länge willkürlich für Viz
        impulse[50] = 1
        kernel_viz = signal.sosfiltfilt(sos, impulse)
    case "sinc":
        # Wir berechnen einen FIR Filter mit der Window-Methode
        # Cutoff festlegen (z.B. relativ zur Nyquist-Frequenz)
        cutoff_hz = st.sidebar.slider(
            "Cutoff (Hz)",
            min_value=100,
            max_value=int(sampling_rate / 2),
            value=2000,
        )

        # Anzahl Taps (Punkte) sollte ungerade sein
        numtaps = window_len if window_len % 2 != 0 else window_len + 1

        # Erstelle Filterkoeffizienten (Hamming Fenster standardmäßig)
        kernel = signal.firwin(
            numtaps,
            cutoff=cutoff_hz,
            fs=sampling_rate,
            window="hamming",
        )

        # Oder besser zentriert:
        sig_filtered = np.convolve(audio_signal, kernel, mode="same")

        kernel_viz = kernel

# 3. VISUALISIERUNG
tab1, tab2 = st.tabs(["📊 Analyse", "🎧 Audio"])

with tab1:
    # FFT via Cache Funktion
    freqs, fft_orig = calculate_fft(audio_signal, sampling_rate)
    _, fft_filt = calculate_fft(sig_filtered, sampling_rate)

    fig = make_subplots(
        rows=2,
        cols=2,
        vertical_spacing=0.15,
        subplot_titles=(
            "Zeitbereich (Zoom)",
            "Frequenzbereich (Original)",
            "Filter Impulsantwort h(n)",
            "Frequenzbereich (Gefiltert)",
        ),
        specs=[[{"colspan": 2}, None], [{}, {}]],
    )

    # Performance: WebGL nutzen ab gewisser Größe
    ScatterType = go.Scattergl if len(t) > 5000 else go.Scatter

    # Zeitbereich: Intelligenten Zoom standardmäßig setzen
    # Bei 44kHz sind 500 Samples nur 0.01s (kaum sichtbar).
    # Wir nehmen standardmäßig z.B. 20ms Fenster.
    zoom_samples = int(0.02 * sampling_rate)
    zoom_samples = max(100, min(zoom_samples, len(t)))

    use_zoom = st.checkbox("Auf 20ms zoomen (Detailansicht)", value=True)

    if use_zoom:
        # Mitte des Signals suchen für interessanten Bereich
        start_idx = len(t) // 4
        sl = slice(start_idx, start_idx + zoom_samples)
        plot_t, plot_orig, plot_filt = t[sl], audio_signal[sl], sig_filtered[sl]
    else:
        # Downsampling für Performance beim Vollbild
        ds = max(1, len(t) // 10000)
        plot_t, plot_orig, plot_filt = t[::ds], audio_signal[::ds], sig_filtered[::ds]
        st.caption(f"Zeige gesamtes Signal ({ds}-fach downsampled)")

    # Plots Zeitbereich
    fig.add_trace(
        ScatterType(x=plot_t, y=plot_orig, name="Original", line=dict(color="silver")),
        row=1,
        col=1,
    )
    fig.add_trace(
        ScatterType(
            x=plot_t, y=plot_filt, name="Gefiltert", line=dict(color="blue", width=1.5)
        ),
        row=1,
        col=1,
    )

    # Plot Impulsantwort
    if kernel_viz is not None:
        x_k = np.arange(len(kernel_viz)) - len(kernel_viz) // 2
        fig.add_trace(
            go.Bar(x=x_k, y=kernel_viz, name="Kernel", marker_color="red"), row=2, col=1
        )

    # Plots Frequenz
    # Limitieren auf Nyquist / 2 für bessere Sichtbarkeit bei Musik
    freq_limit = sampling_rate / 2

    # Um Datenmenge zu reduzieren, schneiden wir das FFT Array für den Plot
    freq_mask = freqs <= freq_limit

    fig.add_trace(
        ScatterType(
            x=freqs[freq_mask],
            y=fft_orig[freq_mask],
            name="FFT Orig",
            line=dict(color="gray"),
        ),
        row=2,
        col=2,
    )
    fig.add_trace(
        ScatterType(
            x=freqs[freq_mask],
            y=fft_filt[freq_mask],
            name="FFT Filt",
            line=dict(color="blue"),
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        height=700, template="plotly_white", margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_yaxes(type="log", title="Log Amp", row=2, col=2)
    fig.update_xaxes(title="Hz", row=2, col=2)

    st.plotly_chart(fig, use_container_width=True)

with tab2:

    def to_wav(sig, fs):
        buf = io.BytesIO()
        # Clip signal to avoid distortion before saving
        # sig_clipped = np.clip(sig, -1.0, 1.0)
        # wavfile.write(buf, int(fs), sig_clipped)
        # wavfile.write(buf, int(fs), sig)
        sig_clipped = np.clip(sig, -1.0, 1.0)
        sig_int16 = (sig_clipped * 32767).astype(np.int16)
        wavfile.write(buf, int(fs), sig_int16)
        return buf

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original")
        st.audio(to_wav(audio_signal, sampling_rate), format="audio/wav")

    with col2:
        st.markdown("### Gefiltert")
        st.audio(to_wav(sig_filtered, sampling_rate), format="audio/wav")
