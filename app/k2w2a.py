# -*- coding: utf-8 -*-

# import re
# import os.path
# import sqlite3
import pandas as pd
import numpy as np
import requests
# import genanki
from bs4 import BeautifulSoup as bs
import lxml
# from time import sleep


class WikiParser:
    # build a word list from frequency database
    def get_word_list():
        file_loc = r"C:\Users\npnew\OneDrive\Documents\dev\k2w2a\app\data\Manulex.xls"
        df = pd.read_excel(file_loc, index_col=None, na_values=[''], usecols = "A,R")
        return df


    # get page content as xml from Wiktionnaire page via the page title
    def get_source(stem):
        # define url
        url_str = "https://fr.wiktionary.org/wiki/%s" % stem
        result = requests.get(url_str)

        # check that page exists
        if result.status_code != 200:
            print("No Wiktionnaire Page for" + stem + ".")
            return None

        return result

    # parse the page content and put relevant text into slots in pd
    def parse_page(page):
        return True

    # initialize an Anki deck
    def make_deck(self):
        return True

    # write an Anki deck to a file
    def write_deck(deck):
        return True

    # create single comp/prod flashcard from pd dataframe
    def make_flashcard(frame):
        return True

    # create single conjugation flashcard from pd DataFrame
    def make_conjugation(frame):
        return True

    # create sentence completion card from text
    def make_sentence(text):
        return True

    def build_db():
        list = WikiParser.get_word_list()
        datab = Database()

        i=0

        for index, row in list.iterrows():
            i = i + 1
            datab.add_page(Page(row['LEMMAS']))
            if i == 30:
                break

        print(datab.db)

    # update a .csv file with words from a Database
    def update_csv(file):
        return True

# object to hold all page information
class Page:
    def __init__(self, word):
        n_variants = 10
        n_defs = 30
        n_sents = 10
        n_pics = 6

        stems = np.array([word] * n_variants)
        total = np.array([x for x in range(0, n_variants)])

        # def-sents is an array of tuples of a definition and one example sentence
        fields = np.array([
            'word', 'freq', 'audio', 'pos', 'nsm', 'nms-ipa', 'nmpl', 'nmpl-ipa',
            'nfs', 'nfs-ipa', 'nfpl', 'nfpl-ipa', 'adjm', 'adjm-ipa', 'adjf',
            'adjf-ipa', 'defs', 'syns', 'ants', 'hypers', 'hypos', 'derivs', 'pics',
            'def-sents'
        ])

        defs = np.array(['def' + str(x) for x in range(0, n_defs)])
        strs = np.array(['str' + str(x) for x in range(0, n_sents)])
        pics = np.array(['pic' + str(x) for x in range(0, n_pics)])

        self.data = pd.DataFrame(index=[stems, total], columns=fields)
        self.stem = word

class Database:
    def __init__(self):
        self.db = pd.DataFrame()

    def add_page(self, Page):
        self.db = pd.concat([self.db, Page.data], axis=0)

    def save_data(self):
        return self

    def read_data(self):
        return self



# card structure (depricated)
# stem | first <b> tag after variants table and images
# freq index
# [pos VARIANT; pos VARIANT; pos VARIANT; pos VARIANT, pos VARIANT] | first <tbody> class after flextable
# IPA | use from <tbody> class, same as above
# pronunciation audio | scrape all .mp3 files
# ====================
# common 1 | common 2 | count number of #fr-nom-x tags
# --------------------
# def 1      def 1    | <ol> objects
# sent 1     sent 1   | <ul> objects
# def 2      def 2
# sent 2     sent 2
# etc        etc
#
# img        img      | <thumbinner> tags
# syns       syns     | id="Synonyms"
# derivs     derivs (as links) | id="Dérivés"
# hyperonyms          | id="Hyperonyms"
# hyponyms            | id="Hyponyms"
