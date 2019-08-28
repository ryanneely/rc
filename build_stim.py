##build_stim.py

##functions to reconstruct a recruitment curve stim pattern

import load_rc
import parse_stim
import utils
import numpy as np

"""
Leaving off 8/27/19

Need to basically just put things together:

- find files in the folder
- order them according to their start time
- extract the stim amplitude
- create scaled versions of the stim trains
- add the stim trains together spaced by their real time differences
- compute some metrics:
    - ordered amp levels, times between stim onsets, pulses per level

"""

def unify_arrays(ts,amps,data,fs=25000,pw=150):
    """
    A function to create one continuous, scaled, data
    array that recreates what the stim pattern was 
    for a series of disparate, separately recorded stimulation epochs
    Args:
        -ts: list of datetime.datetime objects signifying when each stim epoch began
            ***should be in order of occurrence***
        -amps: list of stim amps used in a given epoch (same order as ts)
        -data: stim pattern data arrays, same order as amps
        -fs: the sample frequency of the data, in Hz
        =pw: pulse width of the stimulation phases, in us
    Returns:
        -stim_data: unified and scaled data array, including time gaps
        in between stim epochs
    """
    ##be certian that our timestamps (and thus data) is ordered chronologically
    assert np.all(np.diff(np.argsort(ts))==1)
    ##a container to hold individual data arrays
    arrs = []
    ##start by adding the inter-epoch time and scaling the data. Exclude 
    ##the last array, because it won't have a inter-epoch time
    for i in range(len(ts)-1):
        ##find time (in samples) elapsed between the start of this array and the start of the next
        total_samp = utils.datetime_gaps_to_samples(ts[i],ts[i+1],fs)
        epoch = np.zeros(total_samp) ##initialize the new array
        ##scale the stim array appropriately. Start by identifying the stim on times:
        start,stop,z = parse_stim.get_stim_times(data[i],thresh1=100,thresh2=-100,minimal_dist=500) ##hardcoding these values here for simplicity
        ##now use the stim times as a template and scale appropriately
        scaled = parse_stim.scale_stim(amps[i],z,pw,fs=fs)
        ##insert the scaled stim data array at the beginning of the epoch array
        epoch[0:scaled.size] = scaled
        ##now we can add this to our complete pile
        arrs.append(epoch)
    ##now add in the last stim epoch
    ##scale the stim array appropriately. Start by identifying the stim on times:
    start,stop,z = parse_stim.get_stim_times(data[-1],thresh1=100,thresh2=-100,minimal_dist=500) ##hardcoding these values here for simplicity
    ##now use the stim times as a template and scale appropriately
    scaled = parse_stim.scale_stim(amps[-1],data[-1],pw,fs=fs)
    arrs.append(scaled)
    ##just return everything concatenated together now
    return np.concatenate(arrs)