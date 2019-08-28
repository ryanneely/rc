##parse_stim.py

##functions to parse stimulation information from TDMS files

##by Ryan Neely 8/26/19

import numpy as np
from scipy.signal import find_peaks
import utils


def get_stim_times(stim,thresh1=100,thresh2=-100,minimal_dist=500):
    """
    A function to extract the times at which stimulation occurs
    from the raw recorded waveform. 

    Args:
        -stim: stim data array containing the continuously recorded stim output
        -thresh1: the threshold ABOVE which to consider an active stim pulse. Note 
            that these values have to be set manually.
        -thresh2: the threshold BELOW which to consider an active stim pulse
        -minimal_dist: the minimum distance two waveforms need to be apart from 
            each other in order to be considered a separate train (in samples)
    Returns:
        start_idx: timestamps (scaled in ms) at the start of a stim train
        stop_idx: timestamps (scaled in ms) at the end of a stim train
        z: a waveform showing when the stim train is occurring
    TODO: have some way of determining if this was anodal-first or cathodal-first. 
        I"m thinking you could detect the polarity of the first pulse, and then
        flip the sign of the z-array depending on which type of stimulation you were using.
        This would then propagate down to the scale_stim function. Right now it defaults to anodal-first
    """
    ##get rid of any NaN values from the data; replace with 0's
    to_replace = np.where(np.isnan(stim))[0]
    stim[to_replace] = 0.0
    ##find out where stim is NOT occurring based on the threshold values,
    ##and set these time points to 0
    off = np.where((stim<thresh1)&(stim>thresh2))[0]
    stim[off] = 0
    #now we perform some tricks to figure out where a stim train is taking place
    ##first make a padded version of y
    stim_pad = np.hstack([np.zeros(minimal_dist),stim,np.zeros(minimal_dist)]) 
    ##allocate some memory here
    z = np.zeros(stim.shape)
    ##now we ask: does point n have samples before AND after it in the
    ##minimalDist range that are non-zero? If yes, then it counts as part
    ##of the stim train
    for i in range(z.size):
        if np.any(stim_pad[i:i+minimal_dist+1]) and np.any(stim_pad[i-1+minimal_dist:i+2*minimal_dist]):
            z[i] = 1.0
    ##now, we take the difference between any two points, and the locations where this ==1
    ##is the rising edge, and the locations where this == -1 are the falling edge
    ##TODO: see if this holds in all cases, especially different sample rates
    start_idx = np.where(np.diff(z)==1)[0]
    stop_idx = np.where(np.diff(z)==-1)[0]
    return start_idx, stop_idx, z

def scale_stim(amp,stim,pw,fs=25000):
    """
    A function to scale stimulation patterns by some amplitude.
    Just a way to combine the known amplitude with the stim times. 
    Args:
        -amp (float): amplitude pulse height, assumed to be symmetrical biphasic
        -stim (np.array): array of stim times, with 1 at times stim is on, 0 at other times
        -pw: width of the stim pulse (in microseconds)
        -fs: sample frequency
    """
    ##convert pw to samples
    pw = utils.us_to_samples(pw,fs)
    ##in case our amplitude happens to be 1, make sure that the 
    #stim on value is not equal to our amplitude
    stim = stim*amp*1.5
    pulse_on = np.where(np.diff(stim)>0)[0]
    pulse_off = np.where(np.diff(stim)<0)[0]
    for p in pulse_on:
        stim[p:p+pw] = amp
    for p in pulse_off:
        stim[p:p+pw] = -amp
    ##now anything greater than amp is actually an interpulse interval and 
    ##should be set to 0
    ipi = np.where(stim>amp)[0]
    stim[ipi] = 0
    return stim