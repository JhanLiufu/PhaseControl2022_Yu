"""""""""
Written by Mengzhan Liufu at Yu Lab, University of Chicago
"""""""""
import math
from scipy.signal import sosfiltfilt, sosfilt, filtfilt
import numpy as np


def generate_matrix(regr_buffer_size):
    sampling_axis = np.arange(regr_buffer_size)
    A = np.vstack([sampling_axis, np.ones(len(sampling_axis))]).T
    return A


def calculate_derv(A, filter, Detector):
    curr_filtered = sosfiltfilt(filter, Detector.data_buffer)
    curr_regr = curr_filtered[len(curr_filtered) - Detector.regr_buffer_size:, np.newaxis]
    pinv = np.linalg.pinv(A)
    alpha = pinv.dot(curr_regr)
    return alpha[0][0]


def update_signbuffer(A, filter, Detector):
    curr_derv = calculate_derv(A, filter, Detector)
    Detector.sign_buffer.append(curr_derv > 0)