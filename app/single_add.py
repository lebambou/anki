# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:15:25 2021

@author: npnew
"""

import re
import os.path
import sqlite3
import pandas as pd
import numpy as np
import requests
import genanki
from kindle2anki import k2a

frame = pd.read_csv('word_list.csv')

entries = pd.read_csv('manual_list.txt', encoding='utf-8-sig', header = None)

for word in entries[0]:
    if word not in frame['input'].unique():
        frame = frame.append(k2a.grabInfo(word), ignore_index=True)
        
frame = frame.replace(np.nan, '', regex=True)