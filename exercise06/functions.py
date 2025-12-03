import numpy as np

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
