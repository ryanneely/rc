##load_rc.py

##functions to load recruitment curve data files

##by Ryan Neely 8/26/19

import os
import numpy as np
import nptdms
import re

def parse_files(folder_path):
    """
    a function to collect files and parse information from the file names in a given folder.
    returns a dictionary with stim amplitude:file_path key-value pairs.  

    Note: there are a couple reasons to pull the stim currents from the file name rather than
        the data recorded on the monitor. First, the scaling of the stim monitor from the stimulator
        can be changed at experiment time and there isn't a way to know what the setting was.
        Secondly, because of the sensitivity settings on the DAQ, most of the stim monitor pulses
        rail anyway, so it doesn't really tell you anything.  
    """
    ##first get only the tdms files in the folder
    tdms_files = [x for x in os.listdir(folder_path) if x.endswith(".tdms")]
    ##sub-function that looks in the file name for information about what the stim current was
    def find_stimval(fname):
        #assuming the units are either 'mA' or 'uA'
        try:
            idx_end = re.search("ma",fname,re.IGNORECASE)
            idx_end = idx_end.end()
        except AttributeError:
            idx_end = re.search("ua",fname,re.IGNORECASE)
            idx_end = idx_end.end()
        ##making some assumtions about the file name; basically the numeric current value
        ##will be written immediately prior to the units, and there will be an underscore
        ##before the start of the numeric value. Prototype is "monopolar_1.0ms_1.0ma_001.tdms"
        idx_start = idx_end-1
        while fname[idx_start-1] != "_" and idx_start > 0:
            idx_start -= 1
        return fname[idx_start:idx_end]
    ##now, run through the files, extract the stim value, and join the path and filename 
    result = {}
    for f in tdms_files:
        stimval = find_stimval(f)
        result[stimval] = os.path.join(folder_path,f)
    return result



def get_tstart(tdms_object):
    """
    Function to determine the start time of a tdms file
    Args:
        tdms_object: an open TdmsFile object
    Returns:
        tstart: datetime value
    """
    return tdms_object.property('wf_start_time')

