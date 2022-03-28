# -*- coding: utf-8 -*-

import re
# import os.path
# import sqlite3
import pandas as pd
import numpy as np
import requests
import genanki
from bs4 import BeautifulSoup as bs
import lxml
# from time import sleep
import pdb


class WikiParser:
    # build a word list from frequency database
    def get_word_list(self):
        file_loc = r"I:\anki\Manulex.xls"
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
            # pdb.set_trace()
            if pic.find('img') is not None:
                o_pic_links.append(pic.img['src'])
                print(pic.img['src'])

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

            opts = ['Nom', 'Adjectif', 'Adverbe', 'Verbe', 'Préposition', 'Interjection']
            if any(x in french.text for x in opts):

                # get the POS
                #pdb.set_trace()
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
                    if french.parent.parent.find_next_sibling('table') is not None:

                        item1 = french.parent.parent.find_next_sibling('table')
                        for a in item1.findAll('a'):
                                o_vers.append(a.text)

                    for (ind, out) in zip(o_nouns, o_vers):
                        wordbase.data.loc[(stem, i), ind] = out

                else:
                    # pdb.set_trace()
                    if french.parent.parent.find_next_sibling('p').\
                                                    find(class_='API') is not None:
                        wordbase.data.loc[(stem, i), 'ns-ipa'] = french.parent.\
                                    parent.find_next_sibling('p').find(class_='API').text

                # pdb.set_trace()

                item3 = ''
                if french.parent.parent.find_next(class_='ligne-de-forme') is not None:
                    item3 = french.parent.parent.find_next(class_='ligne-de-forme').text


                # print(french.text + ' ' + item3)
                wordbase.data.loc[(stem, i), 'pos'] = french.text + ' ' + item3

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
                while nextNode is not None:

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
        for i in range(0,23810):
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
    def make_deck(self, frame):
        frame = frame.replace(np.nan, '', regex=True)
        # pdb.set_trace()
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
            5800457367,
            'Français: Vocabulaire v2.0'
            )

        # Vis = 'invisible' for empty entry
        # Vis = '' for valid entry
        my_model = genanki.Model(
            8756083568,
            'Autogen Fr Definition Model v2.0',
            fields = [
                {'name': 'Stem'},
                {'name': 'Freq'},
                {'name': 'IPA'},
                {'name': 'Pic_1'},
                {'name': 'Pic_2'},
                {'name': 'Pic_3'},
                {'name': 'Speech'},
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
                {'name': 'Syns_1'},
                {'name': 'Syns_2'},
                {'name': 'Syns_3'},
                {'name': 'Syns_4'},
                {'name': 'Syns_5'},
                {'name': 'Syns_6'},
                {'name': 'Syns_7'},
                {'name': 'Syns_8'},
                {'name': 'Ants_1'},
                {'name': 'Ants_2'},
                {'name': 'Ants_3'},
                {'name': 'Ants_4'},
                {'name': 'Ants_5'},
                {'name': 'Ants_6'},
                {'name': 'Ants_7'},
                {'name': 'Ants_8'},
                {'name': 'Derivs_1'},
                {'name': 'Derivs_2'},
                {'name': 'Derivs_3'},
                {'name': 'Derivs_4'},
                {'name': 'Derivs_5'},
                {'name': 'Derivs_6'},
                {'name': 'Derivs_7'},
                {'name': 'Derivs_8'},
                {'name': 'Hypers_1'},
                {'name': 'Hypers_2'},
                {'name': 'Hypers_3'},
                {'name': 'Hypers_4'},
                {'name': 'Hypers_5'},
                {'name': 'Hypers_6'},
                {'name': 'Hypers_7'},
                {'name': 'Hypers_8'},
                {'name': 'Hypos_1'},
                {'name': 'Hypos_2'},
                {'name': 'Hypos_3'},
                {'name': 'Hypos_4'},
                {'name': 'Hypos_5'},
                {'name': 'Hypos_6'},
                {'name': 'Hypos_7'},
                {'name': 'Hypos_8'},
                {'name': 'Vis_1'},
                {'name': 'Vis_2'},
                {'name': 'Vis_3'},
                {'name': 'Vis_4'},
                {'name': 'Vis_5'},
                {'name': 'Vis_6'},
                {'name': 'Vis_7'},
                {'name': 'Vis_8'}
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

        lpl = 0
        for key_stem, word_df in frame.groupby(level=0, sort=False):
            lpl = lpl + 1
            print(lpl)

            # take only the first eight entries to avoid duplicates
            word_df = word_df.head(8)

            ipa = word_df.loc[(key_stem, 0), 'ns-ipa'] +\
                  word_df.loc[(key_stem, 0), 'npl-ipa'] +\
                  word_df.loc[(key_stem, 0), 'adjm-ipa'] +\
                  word_df.loc[(key_stem, 0), 'adjmp-ipa']



            # pdb.set_trace()

            # clean up and store defs
            defs = np.empty(8, dtype='object')
            for i in range(8):
                temp = word_df.loc[(key_stem, i), 'defs']
                if type(temp) is not str:
                    # eliminate empty strings
                    temp = temp[np.where(temp != '')]

                    # eliminate extra carriage returns and add one
                    for j in range(len(temp)):
                        temp[j] = temp[j].strip() + '<br>'

                # collapse it all
                temp_tog = ''.join(temp)

                # pdb.set_trace()
                defs[i] = temp_tog

            # clean up and store sents
            sents = np.empty(8, dtype='object')
            for i in range(8):
                # pdb.set_trace()
                temp = word_df.loc[(key_stem, i), 'sents']
                if len(temp) > 0:
                    # eliminate empty strings
                    temp = temp[np.where(temp != '')]

                    # just grab the first sentence for now
                    try:
                        sents[i] = temp[0]
                    except IndexError:
                        sents[i] = ''
                # pdb.set_trace()
                else:
                    sents[i] = ''

            # if lpl == 67:pdb.set_trace()

            pics = word_df.loc[(key_stem, 0), 'pics'][0:3]
            pics_ar = np.empty(3, dtype='object')

            # if lpl == 1241: pdb.set_trace()

            for i in range(3):
                if len(pics) > i:
                    pics_ar[i] = pics[i]
                else: pics_ar[i] = ''

            poses = np.empty(8, dtype = 'object')
            vises = np.empty(8, dtype = 'object')
            for i in range(8):
                poses[i] = word_df.loc[(key_stem, i), 'pos']
                if len(poses[i]) < 1:
                    vises[i] = 'invisible'
                else:
                    vises[i] = ''

            # pdb.set_trace()
            # if lpl == 35: pdb.set_trace()

            synses = np.empty(8, dtype = 'object')
            for i in range(8):
                test = word_df.loc[(key_stem, i), 'syns']
                if len(test) == 0:
                    synses[i] = ''
                else:
                    synses[i] = test[0].replace('\n', ', ')

            antes = np.empty(8, dtype = 'object')
            for i in range(8):
                test = word_df.loc[(key_stem, i), 'ants']
                if len(test) == 0:
                    antes[i] = ''
                else:
                    antes[i] = test[0].replace('\n', ', ')

            derives = np.empty(8, dtype = 'object')
            for i in range(8):
                test = word_df.loc[(key_stem, i), 'derivs']
                if len(test) == 0:
                    derives[i] = ''
                else:
                    derives[i] = test[0].replace('\n', ', ')

            hyperers = np.empty(8, dtype = 'object')
            for i in range(8):
                test = word_df.loc[(key_stem, i), 'hypers']
                if len(test) == 0:
                    hyperers[i] = ''
                else:
                    hyperers[i] = test[0].replace('\n', ', ')

            hypoers = np.empty(8, dtype = 'object')
            for i in range(8):
                test = word_df.loc[(key_stem, i), 'hypos']
                if len(test) == 0:
                    hypoers[i] = ''
                else:
                    hypoers[i] = test[0].replace('\n', ', ')

            my_note = genanki.Note(
                model = my_model,
                fields = [key_stem, # stem
                          str(word_df.loc[(key_stem, 0), 'freq']), # frequency
                          ipa, # ipa
                          pics_ar[0], # pic 1
                          pics_ar[1], # pic 2
                          pics_ar[2], # pic 3
                          word_df.loc[(key_stem, 0), 'audio'], # speech
                          poses[0], # poses
                          poses[1],
                          poses[2],
                          poses[3],
                          poses[4],
                          poses[5],
                          poses[6],
                          poses[7],
                          defs[0], # defs
                          defs[1],
                          defs[2],
                          defs[3],
                          defs[4],
                          defs[5],
                          defs[6],
                          defs[7],
                          sents[0], # sents
                          sents[1],
                          sents[2],
                          sents[3],
                          sents[4],
                          sents[5],
                          sents[6],
                          sents[7],
                          synses[0], # syns
                          synses[1],
                          synses[2],
                          synses[3],
                          synses[4],
                          synses[5],
                          synses[6],
                          synses[7],
                          antes[0], # antes
                          antes[1],
                          antes[2],
                          antes[3],
                          antes[4],
                          antes[5],
                          antes[6],
                          antes[7],
                          derives[0], # derives
                          derives[1],
                          derives[2],
                          derives[3],
                          derives[4],
                          derives[5],
                          derives[6],
                          derives[7],
                          hyperers[0], # hyperers
                          hyperers[1],
                          hyperers[2],
                          hyperers[3],
                          hyperers[4],
                          hyperers[5],
                          hyperers[6],
                          hyperers[7],
                          hypoers[0], # hypoers
                          hypoers[1],
                          hypoers[2],
                          hypoers[3],
                          hypoers[4],
                          hypoers[5],
                          hypoers[6],
                          hypoers[7],
                          vises[0], # vises
                          vises[1],
                          vises[2],
                          vises[3],
                          vises[4],
                          vises[5],
                          vises[6],
                          vises[7],
                          ]
                )

            my_deck.add_note(my_note)

        # %% export card to anki? should be automatic
        # pdb.set_trace()
        genanki.Package(my_deck).write_to_file('data/output.apkg')

    # write an Anki deck to a file
    def write_deck(self, deck):
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
        n_variants = 8

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




# wp = WikiParser()
# frame = wp.get_word_parquet(file_loc='data/wlist.gzip')
# print(frame)
# for index, row in frame.iterrows():
#     print(row)

# pdb.set_trace()

test = WikiParser()
test.word_list_to_parquet()
frame = test.get_word_parquet()
test.parse_many(frame)

frame2 = test.get_word_parquet(file_loc='data/wlist.gzip')
# pdb.set_trace()
# for key_stem, word_df in frame2.groupby(level=0, sort=False):
#     pdb.set_trace()
#     print(key_stem)

test.make_deck(frame2)
