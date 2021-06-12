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

stem = 'botte'

url_str = "https://fr.wiktionary.org/wiki/%s" % stem
result = requests.get(url_str)

# check that page exists
if result.status_code != 200:
    print("No Wiktionnaire Page for" + stem + ".")

# word_entry = pd.Series()

# start each stem as first titredef
# start fresh card if pos changes (e.g. beau adj -> noun)

# change all parsing depending on titredef
# id="fr-nom-x"


soup = bs(result.content, "lxml")

word = soup.main.p.b.text
# find alternate gender version
pos = soup.main.get_next("[class~=titredef]").text

# find second IPA if available
ldf1 = soup.main.p.select("[class~=ligne-de-forme]")[0].text
defs1 = []
sents1 = []

for item in soup.main.ol.findAll('li'):
    for child in item.findAll('ul'):
        # associate each sent with a def
        # probably go ahead and use a multidimensional DataFrame
        sents1.append(child.text)
        child.decompose()

    defs1.append(item.text)

defs1 = list(filter(None, defs1))
#
# print(stem)
# print(ipa1)
# print(ldf1)
# print(' '.join(defs1))



# DataFrame struture
# [stem freq audio] | word, pos, nms, nms-ipa, nmpl, nmpl-ipa, nfs, nfs-ipa, nfpl, nfpl-ipa,
#                   | adjm, adjm-ipa, adjf, adjf-ipa,
#                   | def1, sents1, def2, sents2,...,def30, sents30
#                   | syns, ants, hypers, hypos, derivs, pic1,...,pic5

# stem | first <p> tag after variants table and images
# gender |
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
