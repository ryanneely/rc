##utils.py

##utilities for recruitment curve functions

##by Ryan Neely 8/27/19

import numpy as np

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
