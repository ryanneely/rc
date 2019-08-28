##rc_stats.py

##recreates the full stimulation information from a recruitment curve,
##and computes some statistics about what was done

##by Ryan Neely 8/28/19

import load_rc
import build_stim

def get_stats(f,pw=150,fs=25000):
    """
    Function to create complete recruitment curve information
    from a folder of (only) separately recorded stimulation epoch
    files. 
    Args:
        -f: path to folder containing tdms recording files
        -pw: pulse width of the stimulation phases
        -fs: sample rate of the data
    Returns:
    
    TODO: if I really wanted to, I could extract fs and then also pw from 
        the tdms_object properties
    """
    