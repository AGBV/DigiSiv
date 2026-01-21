import numpy as np
import plotly.graph_objects as go
import scipy.signal.windows as win
import streamlit as st
from plotly.subplots import make_subplots

# --- SEITEN KONFIGURATION ---
st.set_page_config(
    page_title="DSP Labor: Ultimate Windows", layout="wide", page_icon="📡"
)

st.title("📡 Signal-Analyse: High-End Fensterfunktionen")
st.markdown("""
Dieses Tool implementiert die **Cosine-Sum Window Familie** basierend auf Literatur-Koeffizienten.
Formel: $w[n] = \\sum_{k=0}^{K} (-1)^k a_k \\cos(\\frac{2\\pi k n}{N})$
""")

# --- 1. KOEFFIZIENTEN-DATENBANK (Aus Wikipedia extrahiert) ---
# Wir erweitern auf bis zu 5 Koeffizienten [a0, a1, a2, a3, a4]
presets = {
    # Klassiker
    "Rechteck (Boxcar)": [1.0, 0.0, 0.0, 0.0, 0.0],
    "Hann": [0.5, 0.5, 0.0, 0.0, 0.0],
    "Hamming": [0.54, 0.46, 0.0, 0.0, 0.0],
    # Blackman Familie
    "Blackman (Standard)": [0.42, 0.50, 0.08, 0.0, 0.0],
    "Blackman (Exact)": [7938 / 18608, 9240 / 18608, 1430 / 18608, 0.0, 0.0],
    # Low-Sidelobe Fenster (Aus deinem Text)
    "Nuttall (Continuous)": [0.355768, 0.487396, 0.144232, 0.012604, 0.0],
    "Blackman-Nuttall": [0.3635819, 0.4891775, 0.1365995, 0.0106411, 0.0],
    "Blackman-Harris (3-Term)": [0.4243801, 0.4973406, 0.0782793, 0.0, 0.0],
    # Flat Top (5-Term Variante aus Matlab)
    "Flat Top (Matlab)": [
        0.21557895,
        0.41663158,
        0.277263158,
        0.083578947,
        0.006947368,
    ],
}

# --- 2. SESSION STATE MANAGEMENT ---
# Initialisierung
if "coeffs" not in st.session_state:
    st.session_state.coeffs = presets["Hamming"]


# Funktion zum Laden eines Presets in den State
def load_preset():
    # Den Namen aus der Selectbox holen
    name = st.session_state.preset_select
    if name in presets:
        c = presets[name]
        st.session_state.a0 = c[0]
        st.session_state.a1 = c[1]
        st.session_state.a2 = c[2]
        st.session_state.a3 = c[3]
        st.session_state.a4 = c[4]


# Defaults setzen, falls Keys noch nicht existieren
defaults = {"a0": 0.54, "a1": 0.46, "a2": 0.0, "a3": 0.0, "a4": 0.0}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("1. Signal Generator")
    fs = 100.0
    n_points = st.slider("Signal Länge N", 32, 1024, 64, 32)

    c1, c2 = st.columns(2)
    f1 = c1.number_input("Freq 1 [Hz]", 0.0, 45.0, 10.5, step=0.5)
    a_sig1 = c2.number_input("Amp 1", 0.0, 10.0, 1.0, step=0.1)

    c3, c4 = st.columns(2)
    f2 = c3.number_input("Freq 2 [Hz]", 0.0, 45.0, 16.0, step=0.5)
    a_sig2 = c4.number_input("Amp 2", 0.0, 10.0, 0.2, step=0.1)

    noise_level = st.slider("Rauschen (Sigma)", 0.0, 2.0, 0.0, 0.1)

    st.divider()

    st.header("2. Fenster Auswahl")

    # Selectbox mit Callback, der sofort die Slider updated
    st.selectbox(
        "Profil wählen:",
        options=list(presets.keys()),
        index=2,  # Hamming default
        key="preset_select",
        on_change=load_preset,
    )

    st.caption("Koeffizienten ($a_0$ bis $a_4$)")
    # Slider sind direkt mit Session State verknüpft
    st.slider("a0 (DC)", 0.0, 1.0, key="a0", step=0.00001, format="%.5f")
    st.slider("a1 (Cos 2π)", 0.0, 1.0, key="a1", step=0.00001, format="%.5f")
    st.slider("a2 (Cos 4π)", 0.0, 1.0, key="a2", step=0.00001, format="%.5f")
    st.slider("a3 (Cos 6π)", 0.0, 1.0, key="a3", step=0.00001, format="%.5f")
    st.slider("a4 (Cos 8π)", 0.0, 1.0, key="a4", step=0.00001, format="%.5f")

    st.divider()
    use_log_scale = st.toggle("Logarithmische Ansicht (dB)", value=True)


# --- 4. BERECHNUNG ---

# Aktuelle Koeffizienten holen
coeffs = [
    st.session_state.a0,
    st.session_state.a1,
    st.session_state.a2,
    st.session_state.a3,
    st.session_state.a4,
]

# Signal
t = np.arange(n_points) / fs
y_raw = a_sig1 * np.sin(2 * np.pi * f1 * t) + a_sig2 * np.sin(2 * np.pi * f2 * t)
np.random.seed(42)
y_noise = y_raw + noise_level * np.random.randn(n_points)

# Fenster Berechnung (Erweitert auf 5 Terme)
n_vec = np.arange(n_points)
# Vorberechnete Terme für Lesbarkeit und Performance
cos2 = np.cos(2 * np.pi * n_vec / (n_points - 1))
cos4 = np.cos(4 * np.pi * n_vec / (n_points - 1))
cos6 = np.cos(6 * np.pi * n_vec / (n_points - 1))
cos8 = np.cos(8 * np.pi * n_vec / (n_points - 1))

# Formel: Summe (-1)^k * ak * cos(...)
# a0 - a1 + a2 - a3 + a4
w_n = (
    coeffs[0]
    - coeffs[1] * cos2
    + coeffs[2] * cos4
    - coeffs[3] * cos6
    + coeffs[4] * cos8
)

# Fenster anwenden
y_windowed = y_noise * w_n

# FFT
n_fft = 4096  # Hohe Auflösung für glatte Kurven
f_axis = np.fft.fftshift(np.fft.fftfreq(n_fft, d=1 / fs))

# Raw
mag_raw = np.abs(np.fft.fftshift(np.fft.fft(y_noise, n_fft))) / n_points

# Windowed
gain_corr = np.sum(w_n) if np.sum(w_n) > 0 else 1.0
mag_win = np.abs(np.fft.fftshift(np.fft.fft(y_windowed, n_fft))) / gain_corr

# Filter (Positive Frequenzen)
pos_mask = f_axis >= 0
f_plot = f_axis[pos_mask]
y_plot_raw = mag_raw[pos_mask]
y_plot_win = mag_win[pos_mask]


# --- 5. VISUALISIERUNG ---

# Dynamische Y-Achse
if use_log_scale:
    y_min_log = 1e-6  # -120dB
    y_max = max(a_sig1, a_sig2, 1.0) * 1.5
    y_range = [np.log10(y_min_log), np.log10(y_max)]
    axis_type = "log"
    y_title = "Amplitude (Log)"
else:
    y_max = max(a_sig1, a_sig2, 1.0) * 1.2
    y_range = [0, y_max]
    axis_type = "linear"
    y_title = "Amplitude (Linear)"


fig = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=("Zeitbereich", f"Frequenzbereich ({axis_type})"),
    vertical_spacing=0.15,
)

# Plot 1: Zeit
fig.add_trace(
    go.Scatter(
        x=t, y=y_noise, name="Signal (Raw)", line=dict(color="lightgray", width=1)
    ),
    row=1,
    col=1,
)
scale = np.max(np.abs(y_noise)) if np.max(np.abs(y_noise)) > 0 else 1.0
fig.add_trace(
    go.Scatter(
        x=t,
        y=w_n * scale,
        name="Fenster-Hüllkurve",
        line=dict(color="green", dash="dot", width=1.5),
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(x=t, y=y_windowed, name="Gefenstert", line=dict(color="blue", width=2)),
    row=1,
    col=1,
)

# Plot 2: Frequenz
fig.add_trace(
    go.Scatter(
        x=f_plot,
        y=y_plot_raw,
        name="Rechteck",
        line=dict(color="gray", width=1),
        fill="tozeroy",
    ),
    row=2,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=f_plot,
        y=y_plot_win,
        name="Gewähltes Fenster",
        line=dict(color="blue", width=2),
    ),
    row=2,
    col=1,
)

# Marker & Linien
fig.add_trace(
    go.Scatter(
        x=[f1, f2],
        y=[a_sig1, a_sig2],
        mode="markers",
        name="Soll-Werte",
        marker=dict(color="red", symbol="x", size=10, line=dict(width=2)),
        hovertemplate="Freq: %{x} Hz<br>Amp: %{y:.2f}<extra></extra>",
    ),
    row=2,
    col=1,
)

line_bottom = 1e-6 if use_log_scale else 0
for f_target, a_target in zip([f1, f2], [a_sig1, a_sig2]):
    fig.add_shape(
        type="line",
        x0=f_target,
        x1=f_target,
        y0=line_bottom,
        y1=a_target,
        xref="x2",
        yref="y2",
        line=dict(color="red", dash="dash", width=1),
    )
    fig.add_annotation(
        x=f_target,
        y=a_target,
        xref="x2",
        yref="y2",
        text=f"f={f_target}",
        showarrow=False,
        font=dict(color="red"),
        yanchor="bottom",
        yshift=5,
    )

# Layout
fig.update_layout(height=800, template="plotly_white", hovermode="x unified")
fig.update_xaxes(title_text="Zeit [s]", row=1, col=1)
fig.update_xaxes(title_text="Frequenz [Hz]", range=[0, fs / 2], row=2, col=1)
fig.update_yaxes(title_text=y_title, type=axis_type, range=y_range, row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

# --- 6. INFO BOX ---
st.info(f"""
**Aktuelle Koeffizienten:**
$a_0={coeffs[0]:.5f}, a_1={coeffs[1]:.5f}, a_2={coeffs[2]:.5f}, a_3={coeffs[3]:.5f}, a_4={coeffs[4]:.5f}$

**Summe:** {sum(coeffs):.5f}
*(Eine Summe $\\neq 1$ beeinflusst die absolute Amplitude, wird aber durch die Normierung im Plot korrigiert.)*
""")
