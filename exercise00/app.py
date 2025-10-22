import numpy as np
import streamlit as st
from numba import jit, prange
from plotly import graph_objects as go


@jit(nopython=True, nogil=True, parallel=True, cache=True)
def mandelbrot(x, y, maxiter=100):
    mat = np.zeros((x.size, y.size))

    for k in prange(mat.size):
        i = k % x.size
        j = k // x.size

        c = complex(x[i], y[j])
        z = complex(0, 0)

        for n in range(maxiter):
            z = z * z + c
            if z.real * z.real + z.imag * z.imag > 4.0:
                mat[i, j] = n + 1 - np.log(np.log(np.abs(z * z + c))) / np.log(2)
                break

    return mat


x_start = -2
x_end = 1

y_start = -1
y_end = 1

maxiter = st.number_input("Max Iterations", min_value=1, value=100)

x_pixel = st.number_input("Horizontal Pixels", min_value=400, value=800)
y_pixel = np.int64(x_pixel * (y_end - y_start) / (x_end - x_start))

x_vec = np.linspace(x_start, x_end, x_pixel)
y_vec = np.linspace(y_start, y_end, y_pixel)

with st.spinner("Calculating mandelbrot set...", show_time=True):
    mat = mandelbrot(x_vec, y_vec, maxiter)
    mat = np.transpose(mat.reshape((x_pixel, y_pixel)))

fig = go.Figure()
fig.add_trace(
    go.Heatmap(
        z=mat,
        x=x_vec,
        y=y_vec,
        colorscale="Viridis",
    )
)
fig.update_layout(
    height=600,
    yaxis=dict(
        scaleanchor="x",
        scaleratio=1,
    ),
)
st.plotly_chart(fig)
