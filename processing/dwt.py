import pywt
def compute_dwt(signal, wavelet='db4', level=3):
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    return coeffs  # [approximation, details1, details2, ...]
