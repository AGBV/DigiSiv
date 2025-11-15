import lcapy as lc
import matplotlib.pyplot as plt
import streamlit as st
from lcapy import symbol
from numpy import pi

# from lcapy.discretetime import n
# import mpld3
# import streamlit.components.v1 as components

expression = st.text_input(
    label="Enter a discrete-time signal expression in terms of n and w:",
    value="cos(w * n)",
)

w = symbol("w")
signal = lc.expr(expression)
z_transform = signal.ZT()  # pyright: ignore
st.write("Signal: ", signal.expr)
st.write("Z-trans: ", z_transform.expr)  # pyright:ignore

w_sub = st.slider(
    label="Select a value for w (fraction of 2pi in radians):",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
)
w_sub *= 2 * pi
evaluation = signal.subs(w, w_sub)
# st.write(signal.subs(w, w_sub).expr)
st.write(z_transform.subs(w, w_sub).expr)  # pyright: ignore

fig, axes = plt.subplots()
evaluation.plot(axes=axes)  # pyright: ignore
st.pyplot(fig)

fig, axes = plt.subplots()
evaluation.ZT().plot(axes=axes)  # pyright: ignore
st.pyplot(fig)
