# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 18:24:42 2020

@author: npnew
"""
# TODO slim down imports to bare necessities
# TODO reorganize methods to make more sense/flow
# TODO individual word search + add
# TODO webapp or executable
# TODO English translation to French search

import re
import os.path
import sqlite3
import pandas as pd
import numpy as np
import requests
import genanki
from bs4 import BeautifulSoup as bs
import lxml
from time import sleep

class k2a:
    # %% grab headliner from CNRTL
    def grabInfo(stem): # will have df value as argument
        index = 1
        # output populated info
        c_out = pd.DataFrame(columns=["input",
                                      "word_1", "word_2", "word_3", "word_4",
                                      "pos_1", "pos_2", "pos_3", "pos_4",
                                      "def_1", "def_2", "def_3", "def_4",
                                      "sent_1", "sent_2", "sent_3", "sent_4",
                                      "ipa", "pic", "speech"])

        # get words, part of speech, definition, and sentence from CNRTL
        # create URL for search
        # TODO catch when URL fails
        url_str = "https://www.cnrtl.fr/definition/" + stem

        # verify valid page
        result = requests.get(url_str)
        if result.status_code != 200:
            print("No CPFL Links") # this only happens with no connection
            return c_out

        soup = bs(result.content, 'lxml')


        # super hacky, TODO fix this
        # b = type(soup.findAll(class_ = "nonsense"))
        words_out = soup.select('span[class^=tlf_cmot]')

        # get up to four definitions
        i = 0
        while(i < len(words_out) and i < 4):

            col_1 = "word_" + str(i+1)
            col_2 = "pos_" + str(i+1)
            col_3 = "def_" + str(i+1)
            col_4 = "sent_" + str(i+1)

            word_ = words_out[i]
            pos_  = words_out[i].find_next(class_ = "tlf_ccode")
            def_  = words_out[i].find_next(class  = "tlf_cdefinition")
            sent_ = words_out[i].find_next(class_ = "tlf_cexemple")

            if word_ is not None:
                c_out.at[index, col_1] = word_.text
            if pos_ is not None:
                c_out.at[index, col_2] = pos_.text
            if def_ is not None:
                c_out.at[index, col_3] = def_.text
            if sent_ is not None:
                c_out.at[index, col_4] = sent_.text
            i += 1


        # grab ipa and picture from Wiktionary
        # TODO catch when URL fails
        url_str = "https://fr.wiktionary.org/wiki/" + stem
        result = requests.get(url_str)

        if result.status_code != 200:
            print("No Wiktionary Link") # this only happens with no connection
            return c_out

        soup = bs(result.content, "lxml")

        if soup.find(class_="API") is not None:
            c_out.at[index, "ipa"] = soup.find(class_="API").text

        if soup.find(class_="thumbimage") is not None:
            c_out.at[index, "pic"] = soup.find(class_="thumbimage")['src']

        if soup.find("source", src=re.compile('//upload.*\.mp3')) is not None:
            c_out.at[index, "speech"] = soup.find("source",
                                      src=re.compile('//upload.*\.mp3'))["src"]

        c_out.at[index, "input"] = stem

        return c_out

    # %% retrieve vocab db file from kindle
    def updateCSV():
        k_vocab = sqlite3.connect('C:/Users/npnew/OneDrive/Desktop/vocab.db')
        df = pd.read_sql_query("SELECT * FROM words", k_vocab)
        df = df[df.lang == 'fr'].reset_index()

        # grab existing word list
        if not os.path.exists('word_list.csv'):
            tag = False
            frame = pd.DataFrame()
        else:
            tag = True
            frame = pd.read_csv('word_list.csv')

        # fill it up with words
        i = 1
        for word in df['stem']:
            print(i)
            # refill everything if word_list.csv is missing
            if tag == False:
                frame = frame.append(k2a.grabInfo(word), ignore_index=True)
            # new words only
            elif word not in frame['input'].unique():
                frame = frame.append(k2a.grabInfo(word), ignore_index=True)
                i += 1
                print(i)


            if (i == 500):
                break

        # push the results to csv
        frame.to_csv('word_list.csv', encoding='utf-8-sig', index=False)

        return frame

    # %% fill cards -> deck -> export to apkg file
    def buildDeck(self):
        # fill up a datastructure from the .csv, formatting stuff
        # grab existing word list

        if not os.path.exists('word_list.csv'):
            tag = False
            print('File does not exist, execute k2a.updateCSV()')
        else:
            tag = True
            frame = pd.read_csv('word_list.csv')

        frame = frame.replace(np.nan, '', regex=True)

        # read CSS file for card formatting
        css_file = open('styles/card_style.txt')
        css_str = css_file.read()
        css_file.close()

        front_file = open('styles/front_format.txt')
        front_str = front_file.read()
        front_file.close()

        back_file = open('styles/back_format.txt')
        back_str = back_file.read()
        back_file.close()

        front_file_b = open('styles/front_format_b.txt')
        front_str_b = front_file_b.read()
        front_file_b.close()

        back_file_b = open('styles/back_format_b.txt')
        back_str_b = back_file_b.read()
        back_file_b.close()

        # %% make a card object with data from each row of dataframe
        # make sure to check for existing card, no repeats important
        my_deck = genanki.Deck(
            9379226097,
            'Français: Vocabulaire'
            )

        my_model = genanki.Model(
            1178718032 ,
            'Autogen Fr Definition Model',
            fields = [
                {'name': 'Stem'},
                {'name': 'POS_1'},
                {'name': 'POS_2'},
                {'name': 'POS_3'},
                {'name': 'POS_4'},
                {'name': 'POS_5'},
                {'name': 'POS_6'},
                {'name': 'POS_7'},
                {'name': 'POS_8'},
                {'name': 'Def_1'},
                {'name': 'Def_2'},
                {'name': 'Def_3'},
                {'name': 'Def_4'},
                {'name': 'Def_5'},
                {'name': 'Def_6'},
                {'name': 'Def_7'},
                {'name': 'Def_8'},
                {'name': 'Sent_1'},
                {'name': 'Sent_2'},
                {'name': 'Sent_3'},
                {'name': 'Sent_4'},
                {'name': 'Sent_5'},
                {'name': 'Sent_6'},
                {'name': 'Sent_7'},
                {'name': 'Sent_8'},
                {'name': 'Vis_1'},
                {'name': 'Vis_2'},
                {'name': 'Vis_3'},
                {'name': 'Vis_4'},
                {'name': 'Vis_5'},
                {'name': 'Vis_6'},
                {'name': 'Vis_7'},
                {'name': 'Vis_8'},
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
