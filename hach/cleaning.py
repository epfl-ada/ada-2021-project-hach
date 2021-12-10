# imports
import numpy as np
import pandas as pd

def replace_name(q, qids_to_name={}):
    """Replace the aliases for one person by a unique name"""
    if 0 < len(q.qids):
        if q.qids[0] not in qids_to_name:
            qids_to_name[q.qids[0]] = q.speaker
        else:
            q.speaker = qids_to_name[q.qids[0]]
    return q

def clean_df(df):
    """Cleans the dataset for speakers only for now"""
    
    # remove all the 'None' speakers
    df = df[df['speaker'] != 'None']
    
    df = df.apply(replace_name, axis=1)
    
    return df