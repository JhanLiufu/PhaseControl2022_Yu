"""
random_stimulation.py: the random stimulation methods; completely random, or random
sampling from predefined probabilistic distribution
"""
import numpy as np
from random import randrange
from numpy.random import normal, laplace, vonmises


def get_complete_random(sample_count=250):
    """
    Get completely random stimulation

    Parameters
    ----------
    sample_count : int, number of trodes samples that correspond to 2PI

    Returns
    ----------
    int, the number of samples to wait in the current cycle before stimulate
    """
    return randrange(0, sample_count)


def get_vonmises_random(center, kappa, sample_count=250):
    """
    Sample random point from Von Mises (circular normal) distribution to stimulate in the current cycle

    Parameters
    ----------
    center : float, the center of Von Mises distribution
    kappa : float, the dispersion of Von Mises distribution
    sample_count : int, number of trodes samples that correspond to 2Pi

    Returns
    -------
    int, the number of samples to wait in the current cycle before stimulate
    """
    # randomly sample a phase value from von mises (circular normal) distribution
    rand_phase = vonmises(center, kappa)
    # change range from [-PI, PI] to [0, 2PI]
    rand_phase += 2*np.pi*(rand_phase < 0)
    # translate phase to sample count
    return translate_phase_to_sample_count(rand_phase, sample_count)


def get_gaussian_random(center, width, sample_count=250):
    """
    Sample random point from Gaussian/normal distribution to stimulate in the current cycle

    Parameters
    ----------
    center : float, the center of Gaussian/normal distribution
    width : float, the width/standard deviation of Gaussian/normal distribution
    sample_count : int, number of trodes samples that correspond to 2Pi

    Returns
    -------
    int, the number of samples to wait in the current cycle before stimulate
    """
    # randomly sample a phase value from gaussian distribution
    rand_phase = normal(center, width)
    rand_phase = validate_rand_phase(rand_phase)
    # translate phase to sample count
    return translate_phase_to_sample_count(rand_phase, sample_count)


def get_laplace_random(center, scale, sample_count=250):
    """
    Sample random point from Laplace distribution to stimulate in the current cycle

    Parameters
    ----------
    center : float, the center of Laplace distribution
    scale : float, the exponential decay, must be non-negative
    sample_count : int, number of trodes samples that correspond to 2Pi

    Returns
    -------
    int, the number of samples to wait in the current cycle before stimulate
    """
    # randomly sample a phase value from laplace distribution
    rand_phase = laplace(center, scale)
    rand_phase = validate_rand_phase(rand_phase)
    # translate phase to sample count
    return translate_phase_to_sample_count(rand_phase, sample_count)


def validate_rand_phase(rand_phase):
    """
    Correct invalid random phase values (the ones out of 0-2Pi range) generated
    from non-circurlar distribution

    Parameters
    ----------
    rand_phase : float, a random phase value

    Returns
    -------
    float, the corrected random phase value
    """
    # process rand_phase; it might be negative or larger than 2Pi
    # Option 1: make it 0 if smaller than 0, 2Pi if larger than 2PI
    if rand_phase < 0:
        rand_phase = 0
    elif rand_phase > 2*np.pi:
        rand_phase = 2*np.pi

    # Option 2: make it the center if out of range
    # if rand_phase < 0 or rand_phase > 2*np.pi:
    #     rand_phase = center

    # Option 3: not to do anything about rand_phase > 2Pi. know nothing about the
    # length of the next cycle anyway. Only deal with rand_phase < 0
    # if rand_phase < 0:
    #     rand_phase = 0

    return rand_phase


def translate_phase_to_sample_count(rand_phase, sample_count):
    """
    Translate phase value to the number of sample it corresponds to

    Parameters
    ----------
    rand_phase : float, a random phase value
    sample_count : int, number of trodes samples that correspond to 2Pi

    Returns
    -------
    int, number of samples the input phase correspond to
    """
    return int(rand_phase*sample_count/(2*np.pi))