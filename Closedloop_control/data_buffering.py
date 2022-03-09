"""""""""
Written by Mengzhan Liufu at Yu Lab, the University of Chicago, November 2021
"""""""""

from bandpass_filter import bandpass_filter
import numpy as np


def calculate_noise(filter_type, flattened_array, sampling_rate, order, lowcut, highcut, current_sample):
    current_noise_data = bandpass_filter(filter_type, np.append(flattened_array, current_sample), \
                                          sampling_rate, order, lowcut, highcut)

    return abs(current_noise_data[-1])  # return absolute value here


def data_buffering(client, buffer, buffer_size, sampling_freq, noise_lowcut, noise_highcut, noise_threshold):

    for i in range(buffer_size):
        current_sample = client.receive()
        current_data = current_sample['lfpData']
        buffer.append(current_data[3])

    while True:
        current_sample = client.receive()
        current_data = current_sample['lfpData']

        buffer.append(current_data[3])
        buffer.popleft()
