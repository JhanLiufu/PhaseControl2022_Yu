"""""""""
Written by Mengzhan Liufu at Yu Lab, University of Chicago
"""""""""
from scipy.signal import sosfiltfilt
import numpy as np


# TESTED
def generate_matrix(regr_buffer_size):
    sampling_axis = np.arange(regr_buffer_size)
    A = np.vstack([sampling_axis, np.ones(len(sampling_axis))]).T
    return A


# TESTED
def calculate_derv(A, filter, Detector):
    curr_filtered = sosfiltfilt(filter, Detector.data_buffer)
    curr_regr = curr_filtered[len(curr_filtered) - Detector.regr_buffer_size:, np.newaxis]
    pinv = np.linalg.pinv(A)
    alpha = pinv.dot(curr_regr)
    return alpha[0][0]


# TESTED
def update_signbuffer(A, filter, Detector):
    curr_derv = calculate_derv(A, filter, Detector)
    Detector.sign_buffer.append(curr_derv > 0)
    try:
        Detector.sample_count += 1
    except TypeError:
        pass