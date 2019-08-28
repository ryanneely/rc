##utils.py

##utilities for recruitment curve functions

##by Ryan Neely 8/27/19

import numpy as np
import re

def us_to_samples(us,fs):
    """
    Convert us to samples with a known sample rate
    Args:
        us: microseconds
        fs: sample rate
    Returns:
        n_samp: number of samples corresponding to us
    """
    return int(np.round(us*(fs/1000/1000)))

def search_stim(tdms_file):
    """
    Looks through an open TdmsFile to find the address of the stim data
    Args:
        -tdms_file: open nptdms object
    Returns:
        -group (str): group name
        -channel (str): channel name
    """
    ##just try a bunch of cases. ID the group name first:
    try:
        tdms_file.object('Untitled')
        group = 'Untitled'
    except KeyError:
        try: 
            tdms_file.object('Group Name')
            group = 'Group Name'
        except KeyError:
            tdms_file.object("ephys")
            group = "ephys"
    ##now look for the stim channel. ***ASSUMES THIS IS ALWAYS CH7!!!***
    try:
        tdms_file.object(group,'Dev1/ai7')
        channel = 'Dev1/ai7'
    except KeyError:
        try: 
            tdms_file.object(group,'Dev2/ai7')
            channel = 'Dev2/ai7'
        except KeyError:
            tdms_file.object(group,'Dev3/ai7')
            channel = 'Dev3/ai7'
    return group,channel

def standardize_amps(val):
    """
    Takes in a stim amplitude value (str) and returns
    that value scaled to mA
    Args:
        -val (str): stim amp; ie '100uA'
    Returns:
        -stimval (float): float value of stimval scaled to mA
    """
    ##look for an indication that it's already in mA
    if re.search("ma",val,re.IGNORECASE) == None:
        ##if it's not in microamps, we aren't equipped to handle it
        if re.search("ua",val,re.IGNORECASE) == None:
            raise ValueError("Unrecognized units")
        else:
            stimval = float(val[0:3])
            stimval = stimval/1000.0
    ##in this case the stimval is already in mA, so just return the float
    else:
        stimval = float((val)[0:3])
    return stimval

def datetime_gaps_to_samples(dt1,dt2,fs):
    """
    A function that takes at the difference between two datetime.datetime objects
    and converts it to a number of samples given a known sample rate
    Args:
        -dt1: datetime.datetime number 1
        -dt2: datetime.datetime number 2
        -fs: sample rate, in Hz
    Returns: 
        n_samp: number of samples elapsed between the dt1 and dt2
    """
    ##check to see if dt1 occurred before dt2
    if min(dt1,dt2) == dt1:
        diff = dt2-dt1
    else:
        diff = dt1-dt2
    ##convert the difference to seconds
    diff = diff.total_seconds()
    ##now just multiply this by fs to get total samples elapsed
    return int(np.round(diff*fs))

    
    