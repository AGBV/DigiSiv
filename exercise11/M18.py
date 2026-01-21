import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# --- SEITEN KONFIGURATION ---
st.set_page_config(
    page_title="DSP Labor: Fenster & Spektrum", layout="wide", page_icon="📡"
)

st.title("📡 Signal-Analyse: Fensterung & Auflösung")
st.markdown("""
Untersuche den Einfluss von Fensterfunktionen auf die Spektralanalyse.
""")

# --- 1. SESSION STATE ---
defaults = {"a0": 0.54, "a1": 0.46, "a2": 0.0, "a3": 0.0}  # Default: Hamming

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


def set_preset(p0, p1, p2, p3):
    st.session_state.a0 = p0
    st.session_state.a1 = p1
    st.session_state.a2 = p2
    st.session_state.a3 = p3


# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("1. Signal Generator")

    fs = 100.0
    n_points = st.slider("Signal Länge N", 32, 512, 64, 32)

    st.caption("Frequenzkomponenten")
    c1, c2 = st.columns(2)
    f1 = c1.number_input("Freq 1 [Hz]", 0.0, 45.0, 10.5, step=0.5)
    a_sig1 = c2.number_input("Amp 1", 0.0, 10.0, 1.0, step=0.1)

    c3, c4 = st.columns(2)
    f2 = c3.number_input("Freq 2 [Hz]", 0.0, 45.0, 16.0, step=0.5)
    a_sig2 = c4.number_input("Amp 2", 0.0, 10.0, 0.2, step=0.1)

    noise_level = st.slider("Rauschen (Sigma)", 0.0, 2.0, 0.0, 0.1)

    st.divider()

    st.header("2. Fenster Design")

    c_b1, c_b2 = st.columns(2)
    if c_b1.button("Rechteck"):
        set_preset(1.0, 0.0, 0.0, 0.0)
    if c_b2.button("Hann"):
        set_preset(0.5, 0.5, 0.0, 0.0)
    if c_b1.button("Hamming"):
        set_preset(0.54, 0.46, 0.0, 0.0)
    if c_b2.button("Blackman"):
        set_preset(0.42, 0.50, 0.08, 0.0)
    if st.button("Flat Top"):
        set_preset(0.2155, 0.4166, 0.2772, 0.0835)

    st.caption("Koeffizienten Feintuning")
    st.slider("a0", 0.0, 1.0, key="a0", step=0.001)
    st.slider("a1", 0.0, 1.0, key="a1", step=0.001)
    st.slider("a2", 0.0, 1.0, key="a2", step=0.001)
    st.slider("a3", 0.0, 1.0, key="a3", step=0.001)

    st.divider()
    # Toggle für Log-Achse (Steuert jetzt direkt Plotly layout)
    use_log_scale = st.toggle("Logarithmische Y-Achse", value=True)

# --- 3. BERECHNUNG ---

# Warnung bei falscher Summe
coeffs = [
    st.session_state.a0,
    st.session_state.a1,
    st.session_state.a2,
    st.session_state.a3,
]
if not np.isclose(sum(coeffs), 1.0, atol=0.02):
    st.warning(f"⚠️ Koeffizientensumme ist {sum(coeffs):.2f} (nicht 1.0).")

# Signal
t = np.arange(n_points) / fs
y_raw = a_sig1 * np.sin(2 * np.pi * f1 * t) + a_sig2 * np.sin(2 * np.pi * f2 * t)
np.random.seed(42)
y_noise = y_raw + noise_level * np.random.randn(n_points)

# Fenster
n_vec = np.arange(n_points)
term = np.pi * n_vec / (n_points - 1)
w_n = (
    coeffs[0]
    - coeffs[1] * np.cos(2 * term)
    + coeffs[2] * np.cos(4 * term)
    - coeffs[3] * np.cos(6 * term)
)

# Anwendung
y_windowed = y_noise * w_n

# FFT (Nur noch MAGNITUDE berechnen, kein dB Conversion mehr!)
n_fft = 2048
f_axis = np.fft.fftshift(np.fft.fftfreq(n_fft, d=1 / fs))

# Raw
mag_raw = np.abs(np.fft.fftshift(np.fft.fft(y_noise, n_fft))) / n_points

# Windowed
gain_corr = np.sum(w_n) if np.sum(w_n) > 0 else 1.0
mag_win = np.abs(np.fft.fftshift(np.fft.fft(y_windowed, n_fft))) / gain_corr

# Filterung für Plot (positive Frequenzen)
pos_mask = f_axis >= 0
f_plot = f_axis[pos_mask]
y_plot_raw = mag_raw[pos_mask]
y_plot_win = mag_win[pos_mask]


# --- 4. VISUALISIERUNG ---

# Dynamische Y-Achsen Grenzen für Log (0 geht nicht bei Log!)
if use_log_scale:
    # Untergrenze z.B. 10^-5 (-100dB Äquivalent)
    y_range = [1e-5, max(a_sig1, a_sig2, 1.0) * 1.5]
    axis_type = "log"
else:
    y_range = [0, max(a_sig1, a_sig2, 1.0) * 1.2]
    axis_type = "linear"

fig = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=("Zeitbereich", f"Frequenzbereich ({axis_type})"),
    vertical_spacing=0.15,
)

# Zeitbereich
fig.add_trace(
    go.Scatter(
        x=t, y=y_noise, name="Signal (Raw)", line=dict(color="lightgray", width=1)
    ),
    row=1,
    col=1,
)
scale = np.max(np.abs(y_noise)) if np.max(np.abs(y_noise)) > 0 else 1
fig.add_trace(
    go.Scatter(
        x=t,
        y=w_n * scale,
        name="Fenster",
        line=dict(color="green", dash="dot", width=1),
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(x=t, y=y_windowed, name="Gefenstert", line=dict(color="blue", width=2)),
    row=1,
    col=1,
)

# Frequenzbereich (Einfach die linearen Werte plotten!)
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
        name="Fenster Ergebnis",
        line=dict(color="blue", width=2),
    ),
    row=2,
    col=1,
)

# --- MARKER & LINIEN ---
# Viel einfacher: Wir müssen keine log10 Umrechnung mehr machen!
# Plotly setzt den Punkt bei y=1.0 automatisch richtig, egal ob die Achse log oder linear ist.

fig.add_trace(
    go.Scatter(
        x=[f1, f2],
        y=[a_sig1, a_sig2],  # Einfach die Amplitude übergeben
        mode="markers",
        name="Soll-Werte",
        marker=dict(color="red", symbol="x", size=10, line=dict(width=2)),
        hovertemplate="Freq: %{x} Hz<br>Amp: %{y:.2f}<extra></extra>",
    ),
    row=2,
    col=1,
)

# Vertikale Linien (y0, y1 nutzen y_range)
fig.add_shape(
    type="line",
    x0=f1,
    x1=f1,
    y0=y_range[0],
    y1=a_sig1,
    xref="x2",
    yref="y2",
    line=dict(color="red", dash="dash", width=1),
)
fig.add_shape(
    type="line",
    x0=f2,
    x1=f2,
    y0=y_range[0],
    y1=a_sig2,
    xref="x2",
    yref="y2",
    line=dict(color="red", dash="dash", width=1),
)

# Annotationen
fig.add_annotation(
    x=f1,
    y=a_sig1,
    xref="x2",
    yref="y2",
    text="f1",
    showarrow=False,
    font=dict(color="red"),
    yanchor="bottom",
    yshift=5,
)
fig.add_annotation(
    x=f2,
    y=a_sig2,
    xref="x2",
    yref="y2",
    text="f2",
    showarrow=False,
    font=dict(color="red"),
    yanchor="bottom",
    yshift=5,
)


# --- LAYOUT FINISHING ---
fig.update_layout(height=800, template="plotly_white", hovermode="x unified")
fig.update_xaxes(title_text="Zeit [s]", row=1, col=1)
fig.update_yaxes(title_text="Amplitude", row=1, col=1)

fig.update_xaxes(title_text="Frequenz [Hz]", range=[0, fs / 2], row=2, col=1)

# HIER PASSIERT DIE MAGIE: TYPE="LOG"
fig.update_yaxes(
    title_text="Amplitude",
    type=axis_type,
    range=[np.log10(y_range[0]), np.log10(y_range[1])]
    if axis_type == "log"
    else y_range,
    row=2,
    col=1,
)

st.plotly_chart(fig, use_container_width=True)
