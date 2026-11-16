import lcapy as lc
import numpy as np
import streamlit as st
import sympy as sp
from plotly import graph_objects as go
from plotly.subplots import make_subplots


def roots(polynomial: sp.Expr, variable: sp.Symbol) -> np.ndarray:
    poly = sp.Poly(polynomial, variable)
    exact = sp.roots(poly)  # keeps multiple roots exact, e.g. (z - 1)**5
    if sum(exact.values()) == poly.degree():
        return np.array([complex(r) for r, m in exact.items() for _ in range(m)])
    return np.array([complex(r) for r in poly.nroots()])


w = lc.symbol("w")

st.markdown(
    "lcapy's `ZT()` is the **one-sided** z-transform: it sums over $n \\geq 0$, "
    "so every signal is implicitly multiplied by the unit step $u(n)$."
)
expression = st.text_input(
    label="Discrete-time signal in terms of n (and optionally w):",
    value="cos(w * n)",
)
try:
    signal = lc.expr(expression)
    if not signal.is_discrete_time_domain:
        raise ValueError("the expression has to depend on n, e.g. 0.5**n or n**4")
    z_transform = signal.ZT()  # pyright: ignore
except Exception as error:
    st.error(f"Could not transform '{expression}': {error}")
    st.stop()

st.latex(
    rf"x(n) = {sp.latex(signal.sympy)} \quad \circ\!-\!\bullet \quad X(z) = {sp.latex(z_transform.sympy)}"
)

w_sub = st.slider("ω (in multiples of π)", 0.0, 1.0, 0.25, 0.01) * np.pi
samples = st.slider("Number of samples", 5, 60, 30)

evaluated = z_transform.subs(w, w_sub).sympy
if len(evaluated.free_symbols) > 1:
    st.error(
        "Only n and w may appear in the expression; replace other symbols by numbers."
    )
    st.stop()
z = next(iter(evaluated.free_symbols), sp.Symbol("z"))
numerator, denominator = sp.fraction(sp.together(evaluated))
zeros, poles = roots(numerator, z), roots(denominator, z)
radius = max(np.abs(poles), default=0.0)
st.write(
    f"Poles: {np.round(poles, 3).tolist()} — the series converges for |z| > {radius:.3f}"
    + (" (outside the unit circle: the sequence grows)" if radius > 1 + 1e-6 else "")
)

n = np.arange(samples)
values = np.real_if_close(np.asarray(signal.subs(w, w_sub).evaluate(n), dtype=complex))

fig = make_subplots(
    1,
    2,
    subplot_titles=("Sequence x(n)", "Pole-zero diagram of X(z)"),
    column_widths=[0.6, 0.4],
)
fig.add_trace(go.Scatter(x=n, y=values, mode="markers", name="x(n)"), row=1, col=1)
for k, v in zip(n, values, strict=True):
    fig.add_shape(type="line", x0=k, x1=k, y0=0, y1=v, line=dict(width=1), row=1, col=1)
phi = np.linspace(0, 2 * np.pi, 400)
fig.add_trace(
    go.Scatter(
        x=np.cos(phi),
        y=np.sin(phi),
        mode="lines",
        line=dict(color="gray", dash="dot"),
        name="|z| = 1",
    ),
    row=1,
    col=2,
)
if radius > 0:
    fig.add_trace(
        go.Scatter(
            x=radius * np.cos(phi),
            y=radius * np.sin(phi),
            mode="lines",
            line=dict(color="green", width=1),
            name="ROC boundary",
        ),
        row=1,
        col=2,
    )
fig.add_trace(
    go.Scatter(
        x=np.real(zeros),
        y=np.imag(zeros),
        mode="markers",
        marker=dict(symbol="circle-open", size=12),
        name="zeros",
    ),
    row=1,
    col=2,
)
fig.add_trace(
    go.Scatter(
        x=np.real(poles),
        y=np.imag(poles),
        mode="markers",
        marker=dict(symbol="x", size=12),
        name="poles",
    ),
    row=1,
    col=2,
)
fig.update_xaxes(title_text="n", row=1, col=1)
fig.update_xaxes(title_text="Re z", row=1, col=2)
fig.update_yaxes(title_text="Im z", scaleanchor="x2", row=1, col=2)
st.plotly_chart(fig)
