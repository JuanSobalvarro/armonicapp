import numpy as np


def compute_dft(signal: np.ndarray, sample_rate: int):
    """Compute one-sided DFT magnitude for a real signal.

    Returns (freqs, magnitudes).
    """
    n = len(signal)
    if n == 0:
        return np.array([]), np.array([])

    # FFT
    fft_res = np.fft.rfft(signal)
    mags = np.abs(fft_res)

    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)

    return freqs, mags
