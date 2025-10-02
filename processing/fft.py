import numpy as np
def compute_fft(signal):
    fft_coeffs = np.fft.fft(signal)
    return np.abs(fft_coeffs)
