# -*- coding: utf-8 -*-

import re
# import os.path
# import sqlite3
import pandas as pd
import numpy as np
import requests
# import genanki
from bs4 import BeautifulSoup as bs
import lxml
# from time import sleep
import pdb


class WikiParser:
    # build a word list from frequency database
    def get_word_list(self):
        file_loc = r"C:\Users\npnew\OneDrive\Documents\dev\k2w2a\app\data\Manulex.xls"
        df = pd.read_excel(file_loc, index_col=None, na_values=[''],
                            usecols = "A,R")
        return df

    def get_word_parquet(self, file_loc = 'data/Manulex.gzip'):
        df = pd.read_parquet(file_loc)
        return df

    def word_list_to_parquet(self):
        file_loc = r"C:\Users\npnew\OneDrive\Documents\dev\k2w2a\app\data\Manulex.xls"
        df = pd.read_excel(file_loc, index_col=None, na_values=[''],
                            usecols = "A,R")
        df.to_parquet('data/Manulex.gzip', compression ='gzip')

    # get page content as xml from Wiktionnaire page via the page title
    def get_source(self, stem):
        # define url
        url_str = "https://fr.wiktionary.org/wiki/%s" % stem
        result = requests.get(url_str)

        # check that page exists
        if result.status_code != 200:
            print("No Wiktionnaire Page for " + stem + ".")
            return None

        return result

    # parse the page content and put relevant text into slots in pd
    def parse_page(self, stem, freq, webpage, wordbase):
        if webpage is None:
            return None

        o_pic_links = []
        o_speech_links = []
        soup = bs(webpage.content, "lxml")
        i = 0

        # add frequency index first
        wordbase.data.loc[(stem, i), 'freq'] = freq

        # get all picture links
        for pic in soup.findAll(class_='thumbinner'):
            o_pic_links.append(pic.a['href'])
        wordbase.data.loc[(stem, i), 'pics'] = o_pic_links

        # get first pronunciation link
        if soup.find("source", src=re.compile('//upload.*\.mp3')) is not None:
            o_speech_links.append(soup.find("source",
                                      src=re.compile('//upload.*\.mp3'))["src"])
            wordbase.data.loc[(stem, i), 'audio'] = soup.find("source",
                                      src=re.compile('//upload.*\.mp3'))["src"]

        # get variations and number versions
        for french in soup.findAll(id=re.compile('fr-')):
            o_var = []
            o_vers = []

            o_gens = []
            o_defs = []
            o_sents = []
            o_syns = []
            o_derivs = []
            o_ants = []
            o_hypers = []
            o_hypos = []

            o_nouns = ['ns', 'npl', 'ns-ipa', 'npl-ipa',]
            o_verbs = ['adjm', 'adjm-ipa', 'adjmp', 'adjmp-ipa', 'adjf',
                       'adjf-ipa', 'adjfp', 'adjfp-ipa',]

            o_var.append(french.text + '\n')

            if len(french.text) > 3:

                if 'Nom' in french.text:
                    # sing vs plurs and ipa
                    if french.parent.parent.find_next_sibling('table') is not None:

                        item1 = french.parent.parent.find_next_sibling('table')
                        for a in item1.findAll('a'):
                                o_vers.append(a.text)

                    for (ind, out) in zip(o_nouns, o_vers):
                        wordbase.data.loc[(stem, i), ind] = out

                elif 'Adj' in french.text:
                    # sing vs plurs and ipa
                    item1 = french.parent.parent.find_next_sibling('table')
                    for a in item1.findAll('a'):
                        o_vers.append(a.text)

                    for (ind, out) in zip(o_verbs, o_vers):
                        wordbase.data.loc[(stem, i), ind] = out

                else:
                    if french.parent.parent.find_next_sibling('p').\
                                                    find(class_='API') is not None:
                        wordbase.data.loc[(stem, i), 'ns-ipa'] = french.parent.\
                                    parent.find_next_sibling('p').find(class_='API').text

                wordbase.data.loc[(stem, i), 'pos'] = french.text

                # get defs and sents
                item2 = french.parent.parent.find_next_sibling('ol')
                for li in item2.findAll('li'):
                    one_sent_only = True
                    for child in li.findAll('li'):

                        # grab only the first sentence per definition
                        if one_sent_only:
                            o_sents.append(child.text)

                            one_sent_only = False

                        # remove sentence from tree so it doesn't add to def
                        child.decompose()

                    # add definition to defs
                    o_defs.append(li.text)

                wordbase.data.loc[(stem, i), 'defs'] = o_defs
                wordbase.data.loc[(stem, i), 'sents'] = o_sents

                nextNode = french.parent.parent
                while True:
                    nextNode = nextNode.nextSibling
                    try:
                        tag_name = nextNode.name
                    except AttributeError:
                        tag_name = None
                    if tag_name == 'h3':
                        break
                    elif tag_name == 'h4':
                        item = nextNode.findChildren(id=re.compile('Synonymes'))
                        for child in item:
                            if child is not None:
                                o_syns.append(child.parent.find_next('ul').text)
                        wordbase.data.loc[(stem, i), 'syns'] = o_syns

                        item = nextNode.findChildren(id=re.compile('Dérivés'))
                        for child in item:
                            if child is not None:
                                o_derivs.append(child.parent.find_next('ul').text)
                        wordbase.data.loc[(stem, i), 'derivs'] = o_derivs

                        item = nextNode.findChildren(id=re.compile('Antonymes'))
                        for child in item:
                            if child is not None:
                                o_ants.append(child.parent.find_next('ul').text)
                        wordbase.data.loc[(stem, i), 'ants'] = o_ants

                        item = nextNode.findChildren(id=re.compile('Hyperonymes'))
                        for child in item:
                            if child is not None:
                                o_hypers.append(child.parent.find_next('ul').text)
                        wordbase.data.loc[(stem, i), 'hypers'] = o_hypers

                        item = nextNode.findChildren(id=re.compile('Hyponymes'))
                        for child in item:
                            if child is not None:
                                o_hypos.append(child.parent.find_next('ul').text)
                        wordbase.data.loc[(stem, i), 'hypos'] = o_hypos

                i = i + 1

    # parse a word conjugation page
    def parse_conj(self, word):
        return True

    # run the parse over n-length word list and save results to parquet
    def parse_many(self, wordlist):
        o_data = Database()
        for i in range(1170,1200):
            print(i)
            stem, freq = wordlist.loc[i, ['LEMMAS', 'G1-5 U']]
            print(stem + ' ' + str(freq))
            website = self.get_source(stem)
            x = Page(stem)
            self.parse_page(stem, freq, website, x)
            o_data.add_page(x)

        o_data.db.to_parquet('data/wlist.gzip', compression ='gzip')


        pframe = pd.read_parquet('data/wlist.gzip')

        print(pframe)

        return pframe

    # make a deck out of a DataFrame
    def make_deck(self):
        return True

    # write an Anki deck to a file
    def write_deck(self, deck):
        return True

    # create single comp/prod flashcard from pd dataframe
    def make_flashcard(self, frame):
        return True

    # create single conjugation flashcard from pd DataFrame
    def make_conjugation(self, frame):
        return True

    # create sentence completion card from text
    def make_sentence(self, text):
        return True

    def build_db(self):
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

        stems = np.array([word] * n_variants)
        total = np.array([x for x in range(0, n_variants)])

        fields = np.array([
            'freq', 'audio', 'pos', 'ns', 'npl', 'ns-ipa', 'npl-ipa',
            'adjm', 'adjm-ipa', 'adjmp', 'adjmp-ipa', 'adjf', 'adjf-ipa',
            'adjfp', 'adjfp-ipa', 'defs', 'sents', 'syns', 'derivs', 'ants',
            'hypers', 'hypos', 'pics'
        ])

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

wp = WikiParser()
frame = wp.get_word_parquet(file_loc='data/wlist.gzip')
print(frame)

# test = WikiParser()
# frame = test.get_word_parquet()
# test.parse_many(frame)

# stem = 'botte'
# website = WikiParser.get_source(stem)
# x = Page(stem)
# WikiParser.parse_page(stem, website, x)
# # print(x.data)
#
# stem = 'beau'
# website = WikiParser.get_source(stem)
# y = Page(stem)
# WikiParser.parse_page(stem, website, y)
# # print(x.data)
#
# o_data = Database()
# o_data.add_page(x)
# o_data.add_page(y)
#
# print(o_data.db)


# frame = WikiParser.get_word_parquet()
# o_data = Database()
# for i in range(1000,1100):
#     print(i)
#     stem = frame.loc[i, 'LEMMAS']
#     print(stem)
#     website = WikiParser.get_source(stem)
#     x = Page(stem)
#     WikiParser.parse_page(stem, website, x)
#     o_data.add_page(x)
#
#
# o_data.db.to_parquet('data/wlist.gzip', compression ='gzip')
#
#
# pframe = pd.read_parquet('data/wlist.gzip')
#
# print(pframe)
