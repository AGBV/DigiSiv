import numpy as np
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

N = 10000


def transfer_discrete(tau, omega_l, t, n):
    delta_omega = 2 * np.pi / t / n
    omega = np.arange(n) * delta_omega
    transfer_function = -1 / (1 + 1j * omega * tau)

    return omega, transfer_function


def transfer_continuous(tau):
    omega = np.logspace(-3, 3, N)
    return omega, -1 / (1 + 1j * omega * tau)


def impulse_response_discrete(transfer_function_discrete, t):
    h = np.fft.ifft(transfer_function_discrete)
    h = np.real(h)
    h /= t / 2
    return h


def impulse_response_continuous(tau, t_max):
    t = np.linspace(0, t_max, N)
    return t, -1 / tau * np.exp(-t / tau)


n_range = np.logspace(1, 5, 5, base=10, dtype=int)

title = "Implication of parameters on discretization"
st.set_page_config(
    page_title=title,
    layout="wide",
)
st.title(title)
st.write("https://github.com/AGBV/DigiSiV/tree/main/exercie06/MA2.py")

with st.sidebar:
    form = st.form("params")

    tau = form.slider(
        "tau 2",
        min_value=1e-2,
        max_value=1e2,
        value=1.0,
        step=1.0,
    )
    form.divider()

    form.text("System 1")
    omega_l1 = form.slider(
        "omega",
        min_value=1e-2,
        max_value=1e2,
        value=1.0,
        step=1.0,
        key="omega1",
    )
    t_1 = form.slider(
        "T",
        min_value=0.1,
        max_value=1.0,
        value=0.1,
        step=0.05,
        key="t1",
        help="T=2*pi/omega",
    )
    n_1 = form.select_slider("N", n_range, 100, key="n1")

    form.divider()

    form.text("System 2")
    omega_l2 = form.slider(
        "omega",
        min_value=1e-2,
        max_value=1e2,
        value=10.0,
        step=1.0,
        key="omega2",
    )
    t_2 = form.slider(
        "T",
        min_value=0.1,
        max_value=1.0,
        value=0.1,
        step=0.05,
        key="t2",
        help="T=2*pi/omega",
    )
    n_2 = form.select_slider("N", n_range, 100, key="n2")

    submitted = form.form_submit_button("Submit changes")

t_1 *= 2 * np.pi / omega_l1
t_2 *= 2 * np.pi / omega_l2

omega_c, transfer_function_c = transfer_continuous(tau)
omega_1, transfer_function_1 = transfer_discrete(tau, omega_l1, t_1, n_1)
omega_2, transfer_function_2 = transfer_discrete(tau, omega_l2, t_2, n_2)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=omega_c,
        y=np.abs(transfer_function_c),
        name="Continuous",
        line=dict(color="lime", width=4),
    )
)
fig.add_trace(
    go.Scatter(
        x=omega_1[1:],
        y=np.abs(transfer_function_1[1:]),
        name="Discrete 1",
        line=dict(color="red", dash="dot"),
    )
)
fig.add_trace(
    go.Scatter(
        x=omega_2[1:],
        y=np.abs(transfer_function_2[1:]),
        name="Discrete 2",
        line=dict(color="blue", dash="dot"),
    )
)
fig.update_layout(
    title="Bode Plot",
    xaxis=dict(
        title="Frequency [rad/s]",
        type="log",
    ),
    yaxis=dict(
        title="Magnitude",
        type="log",
    ),
)
st.plotly_chart(fig, True)


t_c, h_c = impulse_response_continuous(tau, np.max([n_1 * t_1, n_2 * t_2]))
h_1 = impulse_response_discrete(transfer_function_1, t_1)
h_2 = impulse_response_discrete(transfer_function_2, t_2)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=t_c,
        y=h_c,
        name="Continuous",
        line=dict(color="lime", width=4),
    )
)
fig.add_trace(
    go.Scatter(
        x=np.arange(n_1) * t_1,
        y=h_1,
        name="Discrete 1",
        mode="lines+markers",
        line=dict(color="red", width=1),
    )
)
fig.add_trace(
    go.Scatter(
        x=np.arange(n_2) * t_2,
        y=h_2,
        name="Discrete 2",
        mode="lines+markers",
        line=dict(color="blue", width=1),
    )
)
fig.update_layout(
    title="Impulse Response",
    xaxis=dict(
        title="Time [s]",
        range=[0, tau],
    ),
    yaxis=dict(
        title="h",
    ),
)
st.plotly_chart(fig, True)
