##group_analysis.py

##functions to look at the results of multiple experiments

##by Ryan Neely 8/28/19

import rc_stats
import numpy as np

##basically we just want to create some functions that run the analysis on multiple files,
##and then compile those results into a larger dataset

def batch(f_list,pw=150,fs=25000):
    """
    Runs the analysis on a list of folders, then compiles the results together.
    Args:
        -f_list: list of folders where RC data is stored
    Returns:
        -trains: list of train arrays
        -amps: list of amp arrays
        -gaps: list of gap arrays
        -pulses: list of pulse number arrays
    """
    trains = []
    amps = []
    gaps = []
    pulses = []
    for f in f_list:
        print("processing {}".format(f))
        t,a,g,p = rc_stats.get_stats(f,pw=pw,fs=fs)
        trains.append(t)
        amps.append(a)
        gaps.append(g)
        pulses.append(p)
    return np.asarray(trains),np.asarray(amps),np.asarray(gaps),np.asarray(pulses)

def stats(trains,amps,gaps,pulses):
    """
    Runs statistics on compiled data from multiple experiments
    Args:
        -just the outputs from batch()
    Returns:
        -
    Just to capture my thoughts here; I think we should get the means and standard deviations,
    and maybe build up an average array of stim pulses to plot, just to kind of see where the power is
    maybe some other metrics too?
    """
    ##average lowest amplitude value
    pass
