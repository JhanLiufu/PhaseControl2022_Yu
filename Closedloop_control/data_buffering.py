"""""""""
Written by Mengzhan Liufu at Yu Lab, the University of Chicago
"""""""""
import numpy as np


def data_buffering(lfp_client, dio_client, Detector):
    while True:
        current_data = lfp_client.receive()['lfpData']
        Detector.data_buffer.append(current_data[Detector.target_channel])

        # current_dio = bytearray(dio_client.receive()['digitalData'][0])
        # Detector.trigger = current_dio[Detector.trigger_dio]