from pathlib import Path

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.io
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="Sentinel-2 Explorer")

# --- 1. DATEN LADEN ---
FILE_PATH = Path(__file__).parent / "milazzo_subset.mat"


@st.cache_data
def load_data():
    try:
        mat = scipy.io.loadmat(str(FILE_PATH))
        cube = mat["Mixture"]

        if "BandNames" in mat:
            raw = mat["BandNames"]
            band_names = []
            for item in raw.flat:
                if isinstance(item, np.ndarray) and item.size > 0:
                    band_names.append(str(item.item()).strip())
                elif isinstance(item, (str, np.str_)):
                    band_names.append(item.strip())
                else:
                    band_names.append(str(item).strip())
        else:
            band_names = [f"Band {i + 1}" for i in range(cube.shape[2])]

        wls = mat["Lambda"].flatten()
        return cube, band_names, wls
    except FileNotFoundError:
        return None, None, None


cube, band_names, wls = load_data()

if cube is None:
    st.error(f"Datei nicht gefunden: {FILE_PATH}")
    st.stop()

h, w, b = cube.shape

# --- 2. SIDEBAR ---
st.sidebar.title("Einstellungen")
st.sidebar.header("Bild Vorschau")
view_type = st.sidebar.radio("Modus", ["RGB (True Color)", "Einzelkanal"])

sel_band = None
if view_type == "Einzelkanal":
    sel_band = st.sidebar.selectbox("Kanal", band_names)

st.sidebar.divider()
gain = st.sidebar.slider("Helligkeit (Gain)", 0.5, 10.0, 3.0, 0.1)


def get_idx(name_part):
    for i, n in enumerate(band_names):
        if name_part.lower() in n.lower():
            return i
    return 0


# --- 3. INPUT FORMULAR ---
st.title("🧪 Linear Spectral Unmixing")
st.markdown(
    "Definiere 3 Endmember. Die Berechnung startet erst beim Klick auf den Button."
)

with st.form("unmixing_controls"):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**🔵 EM 1 (z.B. Wasser)**")
        col_x1, col_y1 = st.columns(2)
        x1 = col_x1.number_input("X", 0, w - 1, w // 4, key="x1")
        y1 = col_y1.number_input("Y", 0, h - 1, h // 2, key="y1")

    with c2:
        st.markdown("**🟢 EM 2 (z.B. Veg)**")
        col_x2, col_y2 = st.columns(2)
        x2 = col_x2.number_input("X", 0, w - 1, w // 2, key="x2")
        y2 = col_y2.number_input("Y", 0, h - 1, h // 4, key="y2")

    with c3:
        st.markdown("**🔴 EM 3 (z.B. Stadt)**")
        col_x3, col_y3 = st.columns(2)
        x3 = col_x3.number_input("X", 0, w - 1, 3 * w // 4, key="x3")
        y3 = col_y3.number_input("Y", 0, h - 1, h // 2, key="y3")

    submitted = st.form_submit_button(
        "Berechnen & Anzeigen 🚀", type="primary", use_container_width=True
    )

# --- 4. VISUALISIERUNG & LOGIK ---

if not submitted and "first_run" not in st.session_state:
    st.session_state.first_run = True

# Daten extrahieren
s1 = cube[y1, x1, :]
s2 = cube[y2, x2, :]
s3 = cube[y3, x3, :]

# --- BILD VORSCHAU (NICHT GEFLIPPT) ---
if view_type == "RGB (True Color)":
    bands = [get_idx("Red"), get_idx("Green"), get_idx("Blue")]
    img_preview = cube[:, :, bands]
else:
    img_preview = cube[:, :, band_names.index(sel_band)]

img_preview = np.clip(img_preview * gain, 0, 1)

# HIER: Kein Flip mehr für die Vorschau!
# Plotly 'imshow' erkennt Bilder automatisch und setzt (0,0) nach oben links.

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("1. Vorschau & Lage")

    # px.imshow setzt origin='upper' standardmäßig -> Bild ist korrekt
    fig_map = px.imshow(img_preview, binary_string=True)

    # Marker Koordinaten müssen jetzt NICHT mehr umgerechnet werden
    marker_style = dict(size=12, symbol="x", line=dict(width=2, color="white"))

    fig_map.add_trace(
        go.Scatter(
            x=[x1],
            y=[y1],
            mode="markers",
            name="EM1",
            marker=dict(color="blue", **marker_style),
        )
    )
    fig_map.add_trace(
        go.Scatter(
            x=[x2],
            y=[y2],
            mode="markers",
            name="EM2",
            marker=dict(color="green", **marker_style),
        )
    )
    fig_map.add_trace(
        go.Scatter(
            x=[x3],
            y=[y3],
            mode="markers",
            name="EM3",
            marker=dict(color="red", **marker_style),
        )
    )

    fig_map.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        height=500,
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        showlegend=False,
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_right:
    st.subheader("2. Endmember Spektren")
    fig_em = go.Figure()
    fig_em.add_trace(
        go.Scatter(x=wls, y=s1, name="EM1 (Blau)", line=dict(color="blue", width=2))
    )
    fig_em.add_trace(
        go.Scatter(x=wls, y=s2, name="EM2 (Grün)", line=dict(color="green", width=2))
    )
    fig_em.add_trace(
        go.Scatter(x=wls, y=s3, name="EM3 (Rot)", line=dict(color="red", width=2))
    )

    fig_em.update_layout(
        height=500,
        margin=dict(t=20, b=20),
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_em, use_container_width=True)


# --- BERECHNUNG ---
with st.spinner("Berechne Entmischung..."):
    X_flat = cube.reshape(h * w, b).T
    S = np.column_stack((s1, s2, s3))

    # Unmixing
    S_pinv = np.linalg.pinv(S)
    A_flat = S_pinv @ X_flat

    # Fehler
    X_hat = S @ A_flat
    Resid = X_flat - X_hat
    RMS_flat = np.sqrt(np.mean(Resid**2, axis=0))

    # Reshape
    A_imgs = A_flat.reshape(3, h, w)
    RMS_img = RMS_flat.reshape(h, w)

    # FLIPPING FÜR HEATMAPS
    # Heatmaps (kartesisch) haben (0,0) unten links. Bilder haben Daten (0,0) oben links.
    # Damit die Heatmap aussieht wie das Bild, müssen wir die Daten vertikal spiegeln.
    # A_imgs hat Shape (3, H, W). Wir flippen entlang Axis 1 (Height).
    A_imgs_flipped = np.flip(A_imgs, axis=1)
    RMS_flipped = np.flipud(RMS_img)


# --- ERGEBNIS GRID ---
st.divider()
st.subheader("3. Ergebnisse der Entmischung")

fig_res = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=("Anteil EM 1", "Anteil EM 2", "Anteil EM 3", "Fehler (RMS)"),
    horizontal_spacing=0.1,
    vertical_spacing=0.15,
    shared_xaxes="all",
    shared_yaxes="all",
)


def add_heatmap(data, r, c, cm, title_text, zmax=1.0):
    # Colorbar Positionierung: Links (c=1) -> links außen (-0.15), Rechts (c=2) -> rechts außen (1.02)
    x_pos = -0.15 if c == 1 else 1.02
    y_pos = 0.78 if r == 1 else 0.22

    fig_res.add_trace(
        go.Heatmap(
            z=data,
            colorscale=cm,
            zmin=0,
            zmax=zmax,
            showscale=True,
            colorbar=dict(
                len=0.4,
                x=x_pos,
                y=y_pos,
                yanchor="middle",
                title=dict(text=title_text, side="top"),  # Hier ist der Fix!
                tickfont=dict(size=10),
            ),
        ),
        row=r,
        col=c,
    )


add_heatmap(A_imgs_flipped[0], 1, 1, "Blues", "EM1")
add_heatmap(A_imgs_flipped[1], 1, 2, "Greens", "EM2")
add_heatmap(A_imgs_flipped[2], 2, 1, "Reds", "EM3")

err_max = np.percentile(RMS_flipped, 98)
add_heatmap(RMS_flipped, 2, 2, "Magma", "RMS", zmax=err_max)

fig_res.update_layout(
    height=800,
    # Linker Margin erhöht (80px), damit die linken Colorbars Platz haben
    margin=dict(l=80, r=20, t=40, b=20),
)

fig_res.update_xaxes(showticklabels=False)
fig_res.update_yaxes(showticklabels=False, scaleanchor="x", scaleratio=1)

st.plotly_chart(fig_res, use_container_width=True)
