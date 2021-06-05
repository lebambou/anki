# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 12:03:01 2020

@author: npnew
"""

import re
import os.path
import sqlite3
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import genanki

# %% fill up a datastructure from the .csv, formatting stuff
# grab existing word list

if not os.path.exists('word_list.csv'):
    tag = False
    print('File does not exist, execute k2a.updateCSV()')
else:
    tag = True
    frame = pd.read_csv('word_list.csv')

frame = frame.replace(np.nan, '', regex=True)

# read CSS file for card formatting
css_file = open('card_style.txt')
css_str = css_file.read()
css_file.close()

front_file = open('front_format.txt')
front_str = front_file.read()
front_file.close()

back_file = open('back_format.txt')
back_str = back_file.read()
back_file.close()

front_file_b = open('front_format_b.txt')
front_str_b = front_file_b.read()
front_file_b.close()

back_file_b = open('back_format_b.txt')
back_str_b = back_file_b.read()
back_file_b.close()

# %% make a card object with data from each row of dataframe
# make sure to check for existing card, no repeats important
my_deck = genanki.Deck(
    1098714909,
    'autogen_fr test deck'
    )

my_model = genanki.Model(
    2125051572,
    'Autogen Fr Definition Model',
    fields = [
        {'name': 'Stem'},
        {'name': 'Word_1'},
        {'name': 'Word_2'},
        {'name': 'Word_3'},
        {'name': 'Word_4'},
        {'name': 'POS_1'},
        {'name': 'POS_2'},
        {'name': 'POS_3'},
        {'name': 'POS_4'},
        {'name': 'Def_1'},
        {'name': 'Def_2'},
        {'name': 'Def_3'},
        {'name': 'Def_4'},
        {'name': 'Sent_1'},
        {'name': 'Sent_2'},
        {'name': 'Sent_3'},
        {'name': 'Sent_4'},     
        {'name': 'IPA'},
        {'name': 'Pic'},
        {'name': 'Speech'}
        ],
    templates = [
        {'name': 'Comprehension',
         'qfmt': front_str,
         'afmt': back_str,
         },
        {'name': 'Production',
         'qfmt': front_str_b,
         'afmt': back_str_b
         }
        ],
    css = css_str
    )

for index, row in frame.iterrows():
    my_note = genanki.Note(
        model = my_model,
        fields = [row['input'],
                  row['word_1'],
                  row['word_2'],
                  row['word_3'],
                  row['word_4'],
                  row['pos_1'],
                  row['pos_2'],
                  row['pos_3'],
                  row['pos_4'], 
                  row['def_1'],
                  row['def_2'],
                  row['def_3'],
                  row['def_4'],
                  row['sent_1'],
                  row['sent_2'],
                  row['sent_3'],
                  row['sent_4'],
                  row['ipa'],
                  row['pic'],
                  row['speech']
                  ]
        )
    my_deck.add_note(my_note)
    
# %% export card to anki? should be automatic
genanki.Package(my_deck).write_to_file('output.apkg')

