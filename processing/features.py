import numpy as np
from processing.fft import compute_fft
from processing.dwt import compute_dwt

feature_names = [
    'radar_presence', 'radar_distance',
    'mic_peak', 'mic_mean', 'mic_fft_peak',
    'mic_dwt1_mean', 'mic_dwt1_std',
    'acc_x_mean', 'acc_x_var', 'acc_x_fft_peak',
    'acc_x_dwt1_mean', 'acc_x_dwt1_std', # Repeat for acc_y and acc_z as per your need
]

def extract_features(radar_data, mic_samples, acc_x, acc_y, acc_z):
    # Radar features
    features = [radar_data['presence'], radar_data['distance_m']]
    # Microphone features
    mic_peak = np.max(np.abs(mic_samples))
    mic_mean = np.mean(mic_samples)
    mic_fft_peak = np.max(compute_fft(mic_samples))
    mic_dwt = compute_dwt(mic_samples)
    mic_dwt1_mean = np.mean(mic_dwt[-3])
    mic_dwt1_std = np.std(mic_dwt[-3])
    features += [mic_peak, mic_mean, mic_fft_peak, mic_dwt1_mean, mic_dwt1_std]
    # Accelerometer features - X
    acc_x_mean = np.mean(acc_x)
    acc_x_var = np.var(acc_x)
    acc_x_fft_peak = np.max(compute_fft(acc_x))
    acc_x_dwt = compute_dwt(acc_x)
    acc_x_dwt1_mean = np.mean(acc_x_dwt[-3])
    acc_x_dwt1_std = np.std(acc_x_dwt[-3])
    features += [acc_x_mean, acc_x_var, acc_x_fft_peak, acc_x_dwt1_mean, acc_x_dwt1_std]
    # You can similarly unpack for acc_y and acc_z for a full feature set
    return features
