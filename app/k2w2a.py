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
    def get_word_list():
        file_loc = r"C:\Users\npnew\OneDrive\Documents\dev\k2w2a\app\data\Manulex.xls"
        df = pd.read_excel(file_loc, index_col=None, na_values=[''],
                            usecols = "A,R")
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
    def parse_page(stem, webpage, wordbase):
        soup = bs(webpage.content, "lxml")


        i = 0

        # get all picture links
        # for pic in soup.findAll(class_='thumbinner'):
        #     o_pic_links.append(pic.a['href'])
        #     # print(pic.a['href'])
        # wordbase.data.loc[(stem, i), 'pics'] = o_pic_links
        #
        # if soup.find("source", src=re.compile('//upload.*\.mp3')) is not None:
        #     o_speech_links.append(soup.find("source",
        #                               src=re.compile('//upload.*\.mp3'))["src"])
        #     wordbase.data.loc[(stem, i), 'audio'] = soup.find("source",
        #                               src=re.compile('//upload.*\.mp3'))["src"]

        # get variations and number versions
        for french in soup.findAll(id=re.compile('fr-')):
            o_var = []
            o_vers = []
            o_pic_links = []
            o_speech_links = []
            o_gens = []
            o_defs = []
            o_sents = []
            o_syns = []
            o_derivs = []
            o_ants = []
            o_hypers = []
            o_hypos = []

            o_var.append(french.text + '\n')
            ###

            if 'Nom' in french.text:
                print(french.text)

                # sing vs plurs and ipa
                item1 = french.parent.parent.find_next_sibling('table')
                for a in item1.findAll('a'):
                    o_vers.append(a.text)
                    # print(a.text)

                # variants
                if french.parent.parent.find_next_sibling('p').\
                                    find(class_='ligne-de-forme') is not None:
                    o_gens.append(french.parent.parent.find_next_sibling('p').\
                                            find(class_='ligne-de-forme').text)

            elif 'Adj' in french.text:
                print(french.text)

                # sing vs plurs and ipa
                item1 = french.parent.parent.find_next_sibling('table')
                for a in item1.findAll('a'):
                    o_vers.append(a.text)
                    # print(a.text)

                # gender
                if french.parent.parent.find_next_sibling('p').\
                                    find(class_='ligne-de-forme') is not None:
                    o_gens.append(french.parent.parent.find_next_sibling('p').\
                                            find(class_='ligne-de-forme').text)

            elif 'Verbe' in french.text:
                print(french.text)

                if french.parent.parent.find_next_sibling('p').\
                                    find(class_='ligne-de-forme') is not None:
                    o_gens.append(french.parent.parent.find_next_sibling('p').\
                                  find(class_='ligne-de-forme').text)

            else:
                print(french.text)

                if french.parent.parent.find_next_sibling('p')\
                                    .find(class_='ligne-de-forme') is not None:
                    o_gens.append(french.parent.parent.find_next_sibling('p')\
                                  .find(class_='ligne-de-forme').text)

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
                # print(li.text)

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
                            # print(child.parent.find_next('ul').text)
                    wordbase.data.loc[(stem, i), 'syns'] = o_syns

                    item = nextNode.findChildren(id=re.compile('Dérivés'))
                    for child in item:
                        if child is not None:
                            o_derivs.append(child.parent.find_next('ul').text)
                            # print(child.parent.find_next('ul').text)
                    wordbase.data.loc[(stem, i), 'derivs'] = o_derivs

                    item = nextNode.findChildren(id=re.compile('Antonymes'))
                    for child in item:
                        if child is not None:
                            o_ants.append(child.parent.find_next('ul').text)
                            # print(child.parent.find_next('ul').text)
                    wordbase.data.loc[(stem, i), 'ants'] = o_ants

                    item = nextNode.findChildren(id=re.compile('Hyperonymes'))
                    for child in item:
                        if child is not None:
                            o_hypers.append(child.parent.find_next('ul').text)
                            # print(child.parent.find_next('ul').text)
                    wordbase.data.loc[(stem, i), 'hypers'] = o_hypers

                    item = nextNode.findChildren(id=re.compile('Hyponymes'))
                    for child in item:
                        if child is not None:
                            o_hypos.append(child.parent.find_next('ul').text)
                            # print(child.parent.find_next('ul').text)
                    wordbase.data.loc[(stem, i), 'hypos'] = o_hypos

            if len(french.text) > 3:
                wordbase.data.loc[(stem, i), 'pos'] = french.text
                i = i + 1



    # parse a word conjugation page
    def parse_conj(word):

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
            'word', 'freq', 'audio', 'pos', 'ns', 'ns-ipa', 'npl', 'npl-ipa',
            'adjm', 'adjm-ipa', 'adjf', 'adjf-ipa', 'adjmp', 'adjmp-ipa',
            'adjfp', 'adjfp-ipa', 'defs', 'sents', 'syns', 'derivs', 'ants',
            'hypers', 'hypos', 'pics'
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

stem = 'botte'
website = WikiParser.get_source(stem)
x = Page(stem)
WikiParser.parse_page(stem, website, x)
print(x.data)
# pdb.set_trace()
# print(WikiParser.get_word_list())

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
