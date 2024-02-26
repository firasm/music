import numpy as np
from .fade import fade
from .loud import loud
from ..synths.notes import note_with_vibrato


def adsr(envelope_duration=2, attack_duration=20,
         decay_duration=20, sustain_level=-5,
         release_duration=50, transition="exp", alpha=1,
         db_dev=-80, to_zero=1, number_of_samples=0, sonic_vector=0,
         sample_rate=44100):
    """
    Synthesize an ADSR envelope.
    
    ADSR (Atack, Decay, Sustain, Release) is a very traditional
    loudness envelope in sound synthesis [1].
    
    Parameters
    ----------
    envelope_duration : scalar
        The duration of the envelope in seconds.
    attack_duration : scalar
        The duration of the Attack in milliseconds.
    decay_duration : scalar
        The duration of the Decay in milliseconds.
    sustain_level : scalar
        The Sustain level after the Decay in decibels.
        Usually negative.
    release_duration : scalar
        The duration of the Release in milliseconds.
    transition : string
        "exp" for exponential transitions of amplitude 
        (linear loudness).
        "linear" for linear transitions of amplitude.
    alpha : scalar or array_like
        An index to make the exponential fade slower or faster [1].
        Ignored it transitions="linear" or alpha=1.
        If it is an array_like, it should hold three values to be used
        in Attack, Decay and Release.
    db_dev : scalar or array_like
        The decibels deviation to reach before using a linear fade
        to reach zero amplitude.
        If it is an array_like, it should hold two values,
        one for Attack and another for Release.
        Ignored if trans="linear".
    to_zero : scalar or array_like
        The duration in milliseconds for linearly departing from zero
        in the Attack and reaching the value of zero at the end
        of the Release.
        If it is an array_like, it should hold two values,
        one for Attack and another for Release.
        Is ignored if trans="linear".
    number_of_samples : integer
        The number of samples of the envelope.
        If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the ADSR envelope to be applied to.
        If supplied, d and nsamples are ignored.
    sample_rate : integer
        The sample rate.

    Returns
    -------
    AD : ndarray
        A numpy array where each value is a value of
        the envelope for the PCM samples if sonic_vector is 0.
        If sonic_vector is input,
        AD is the sonic vector with the ADSR envelope applied to it.

    See Also
    --------
    T : An oscillation of loudness.
    L : A loudness transition.
    F : A fade in or fade out.

    Examples
    --------
    >>> W(V()*AD())  # writes a WAV file of a note with ADSR envelope
    >>> s = H( [V()*AD(A=i, R=j) for i, j in zip([6, 50, 300], [100, 10, 200])] )  # OR
    >>> s = H( [AD(A=i, R=j, sonic_vector=V()) for i, j in zip([6, 15, 100], [2, 2, 20])] )
    >>> envelope = AD(d=440, A=10e3, D=0, R=5e3)  # a lengthy envelope

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the 
    discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if type(sonic_vector) in (np.ndarray, list):
        Lambda = len(sonic_vector)
    elif number_of_samples:
        Lambda = number_of_samples
    else:
        Lambda = int(envelope_duration * sample_rate)
    Lambda_A = int(attack_duration * sample_rate * 0.001)
    Lambda_D = int(decay_duration * sample_rate * 0.001)
    Lambda_R = int(release_duration * sample_rate * 0.001)

    perc = to_zero / attack_duration
    attack_duration = fade(fade_out=0, method=transition, alpha=alpha, dB=db_dev, perc=perc, number_of_samples=Lambda_A)

    decay_duration = loud(trans_dev=sustain_level, method=transition, alpha=alpha, number_of_samples=Lambda_D)

    a_S = 10 ** (sustain_level / 20.)
    sustain_level = np.ones(Lambda - (Lambda_A + Lambda_R + Lambda_D)) * a_S

    perc = to_zero / release_duration
    release_duration = fade(method=transition, alpha=alpha, dB=db_dev, perc=perc, number_of_samples=Lambda_R) * a_S

    AD = np.hstack((attack_duration, decay_duration, sustain_level, release_duration))
    if type(sonic_vector) in (np.ndarray, list):
        return sonic_vector * AD
    else:
        return AD


def adsr_vibrato(note_dict={}, adsr_dict={}):
    return adsr(sonic_vector=note_with_vibrato(**note_dict), **adsr_dict)

def adsr_stereo(duration=2, attack_duration=20, decay_duration=20,
                sustain_level=-5, release_duration=50, transition="exp", alpha=1,
                db_dev=-80, to_zero=1, number_of_samples=0, sonic_vector=0, sample_rate=44100):
    """
    A shorthand to make an ADSR envelope for a stereo sound.

    See ADSR() for more information.

    """
    if type(sonic_vector) in (np.ndarray, list):
        sonic_vector1 = sonic_vector[0]
        sonic_vector2 = sonic_vector[1]
    else:
        sonic_vector1 = 0
        sonic_vector2 = 0
    s1 = adsr(envelope_duration=duration, attack_duration=attack_duration, decay_duration=decay_duration, sustain_level=sustain_level, release_duration=release_duration, transition=transition, alpha=alpha,
              db_dev=db_dev, to_zero=to_zero, number_of_samples=number_of_samples, sonic_vector=sonic_vector1, sample_rate=sample_rate)
    s2 = adsr(envelope_duration=duration, attack_duration=attack_duration, decay_duration=decay_duration, sustain_level=sustain_level, release_duration=release_duration, transition=transition, alpha=alpha,
              db_dev=db_dev, to_zero=to_zero, number_of_samples=number_of_samples, sonic_vector=sonic_vector2, sample_rate=sample_rate)
    s = np.vstack((s1, s2))
    return s
