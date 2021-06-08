# -*- coding: utf-8 -*-

# import re
# import os.path
# import sqlite3
import pandas as pd
# import numpy as np
import requests
# import genanki
from bs4 import BeautifulSoup as bs
import lxml
# from time import sleep


class WikiParser:
    def __init__(self):
        return(self)

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

    # check to make sure it is not a derivative of a parent word
    # return highest parent word UNLESS given override
    def find_parent(page):
        return True

    # parse the page content and put relevant text into slots in pd Series
    # build the Series on the fly
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

    # update a .csv file with words from a kindle.db
    def update_csv(file):
        return True


# DataFrame struture
# stem freq audio | word, pos, nms, nms-ipa, nmpl, nmpl-ipa, nfs, nfs-ipa, nfpl, nfpl-ipa,
#                 | adjm, adjm-ipa, adjf, adjf-ipa,
#                 | def1, sents1, def2, sents2,...,def30, sents30
#                 | syns, ants, hypers, hypos, derivs, pic1,...,pic5


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
