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

stem = 'roger'

url_str = "https://fr.wiktionary.org/wiki/%s" % stem
result = requests.get(url_str)

# check that page exists
if result.status_code != 200:
    print("No Wiktionnaire Page for" + stem + ".")

soup = bs(result.content, "lxml")

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

# 'word!', 'freq!', 'audio', 'pos!', 'ns!', 'ns-ipa!', 'npl!', 'npl-ipa!',
# 'adjm!', 'adjm-ipa!', 'adjf!', 'adjf-ipa!', 'adjmp!', 'adjmp-ipa!', 'adjfp!',
# 'adjfp-ipa!', 'defs!', 'sents!', 'syns!', 'derivs!', 'ants!', 'hypers!',
# 'hypos!', 'pics'


# get variations and number versions
for french in soup.findAll(id=re.compile('fr-')):
    o_var.append(french.text + '\n')

    if 'Nom' in french.text:
        print(french.text)

        # sing vs plurs and ipa
        item1 = french.parent.parent.find_next_sibling('table')
        for a in item1.findAll('a'):
            o_vers.append(a.text)
            # print(a.text)

        # variants
        if french.parent.parent.find_next_sibling('p').find(class_='ligne-de-forme') is not None:
            o_gens.append(french.parent.parent.find_next_sibling('p').find(class_='ligne-de-forme').text)

    elif 'Adj' in french.text:
        print(french.text)

        # sing vs plurs and ipa
        item1 = french.parent.parent.find_next_sibling('table')
        for a in item1.findAll('a'):
            o_vers.append(a.text)
            # print(a.text)

        # gender
        if french.parent.parent.find_next_sibling('p').find(class_='ligne-de-forme') is not None:
            o_gens.append(french.parent.parent.find_next_sibling('p').find(class_='ligne-de-forme').text)

    elif 'Verbe' in french.text:
        print(french.text)

        if french.parent.parent.find_next_sibling('p').find(class_='ligne-de-forme') is not None:
            o_gens.append(french.parent.parent.find_next_sibling('p').find(class_='ligne-de-forme').text)

    else:
        print(french.text)

        if french.parent.parent.find_next_sibling('p').find(class_='ligne-de-forme') is not None:
            o_gens.append(french.parent.parent.find_next_sibling('p').find(class_='ligne-de-forme').text)

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

            item = nextNode.findChildren(id=re.compile('Dérivés'))
            for child in item:
                if child is not None:
                    o_derivs.append(child.parent.find_next('ul').text)
                    # print(child.parent.find_next('ul').text)

            item = nextNode.findChildren(id=re.compile('Antonymes'))
            for child in item:
                if child is not None:
                    o_ants.append(child.parent.find_next('ul').text)
                    # print(child.parent.find_next('ul').text)

            item = nextNode.findChildren(id=re.compile('Hyperonymes'))
            for child in item:
                if child is not None:
                    o_hypers.append(child.parent.find_next('ul').text)
                    # print(child.parent.find_next('ul').text)

            item = nextNode.findChildren(id=re.compile('Hyponymes'))
            for child in item:
                if child is not None:
                    o_hypos.append(child.parent.find_next('ul').text)
                    # print(child.parent.find_next('ul').text)


# get all picture links
for pic in soup.findAll(class_='thumbinner'):
    o_pic_links.append(pic.a['href'])
    # print(pic.a['href'])

if soup.find("source", src=re.compile('//upload.*\.mp3')) is not None:
    o_speech_links.append(soup.find("source",
                              src=re.compile('//upload.*\.mp3'))["src"])

# print(o_speech_links)
#
# print(o_defs)
print(o_vers)
