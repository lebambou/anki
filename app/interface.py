# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:39:42 2021

@author: npnew
"""

# TODO align boxes
# TODO database.csv not found, would you like to make one?
# TODO also wait for an 'Enter' press to accept form input
# TODO assign methods to each button
# TODO get translation working... somehow
# TODO README box
# TODO display existing word_list.csv and output.apkg as clickable links
# TODO add info button to each line (where to find kindle db, how to format)
# TODO add exception handlers for all inputs
# TODO add exception handlers for internet connection errors
# TODO add exception handlers for 
# TODO restrict input types in entries to appropriate .txt, .db etc
# TODO comment everything
# TODO get someone to try it on their system
# TODO verify single word input with dialogue box. "is this what you meant?"
# TODO clean up messy .txt list inputs?
# TODO upload project to Github

import tkinter as tk
from tkinter import filedialog as fd
import kindle2anki as k2a
import os.path
import sqlite3
import pandas as pd
import numpy as np
import requests
import genanki

# %% globals

root = tk.Tk()
root.geometry("500x600")

ent1_var = tk.StringVar()
ent2_var = tk.StringVar()
ent3_var = tk.StringVar()
ent4_var = tk.StringVar()
ent5_var = tk.StringVar()

# %% button press handler methods

# %% method 1: single word
def method1(event=None):
    # if not os.path.exists('database.csv'):
    #         tag = False
    #         frame = pd.DataFrame()
    #         # ask if they would like to make a fresh database
    # else:
    #     tag = True
    #     frame = pd.read_csv('database.csv')
    
    word = ent1_var.get()
    print(word)
    
    
    
# %% method 2: word list as .txt
def method2a(event=None):
    filename = fd.askopenfilename()
    ent2.insert(tk.END, filename)
    
def method2b(event=None):
    word = ent2_var.get()
    print(word)
    
    

# %% method 3: vocab.db upload
def method3a(event=None):
    filename = fd.askopenfilename()
    ent3.insert(tk.END, filename)

def method3b(event=None):
    word = ent3_var.get()
    print(word)
    
# %% method 4: single English word
def method4(event=None):
    word = ent4_var.get()
    print(word)
 
    
# %% method 5: English word list
def method5a(event=None):
    filename = fd.askopenfilename()
    ent5.insert(tk.END, filename)
    
def method5b(event=None):
    word = ent2_var.get()
    print(word)

# %% frames
mainframe = tk.Frame(root)
mainframe.pack()

box1 = tk.Frame(root)
box1.pack()

box2 = tk.Frame(root)
box2.pack()

box3 = tk.Frame(root)
box3.pack()

box4 = tk.Frame(root)
box4.pack()

box5 = tk.Frame(root)
box5.pack()

# %% mainframe content
welcome_message = tk.Label(mainframe, text = "Kindle 2 Anki")
welcome_message.pack()


# %% box1 content: single word

desc1 = tk.Label(box1, text = "Import One Word:")
desc1.pack(padx = 5, pady = 20, side = tk.LEFT)

ent1=tk.Entry(box1, textvariable = ent1_var, width = 40)
ent1.pack(padx = 4, pady = 20,
          side = tk.LEFT)

button1 = tk.Button(box1, text = 'Submit',
                   command = method1)
button1.pack(padx = 3, pady = 3, side = tk.LEFT)

# %% box2 content: word list as .txt

desc2 = tk.Label(box2, text = "Import Word List:")
desc2.pack(padx = 5, pady = 20, side = tk.LEFT)

ent2=tk.Entry(box2, textvariable = ent2_var, width = 40)
ent2.pack(padx = 4, pady = 20,
          side = tk.LEFT)

button2a = tk.Button(box2, text = '...',
                   command = method2a)
button2a.pack(padx = 3, pady = 3, side = tk.LEFT)

button2b = tk.Button(box2, text = 'Submit',
                   command = method2b)
button2b.pack(padx = 3, pady = 3, side = tk.LEFT)

# %% box3 content: vocab.db upload

desc3 = tk.Label(box3, text = "Import Kindle.db:")
desc3.pack(padx = 5, pady = 20, side = tk.LEFT)

ent3=tk.Entry(box3, textvariable = ent3_var, width = 40)
ent3.pack(padx = 4, pady = 20,
          side = tk.LEFT)

button3a = tk.Button(box3, text = '...',
                   command = method3a)
button3a.pack(padx = 3, pady = 3, side = tk.LEFT)

button3b = tk.Button(box3, text = 'Submit',
                   command = method3b)
button3b.pack(padx = 3, pady = 3, side = tk.LEFT)

# %% box4 content: single English word

desc4 = tk.Label(box4, text = "Import English Word:")
desc4.pack(padx = 5, pady = 20, side = tk.LEFT)

ent4 = tk.Entry(box4, textvariable = ent4_var, width = 40)
ent4.pack(padx = 4, pady = 20,
          side = tk.LEFT)

button4 = tk.Button(box4, text = 'Submit',
                   command = method4)
button4.pack(padx = 3, pady = 3, side = tk.LEFT)

# %% box5 content

desc5 = tk.Label(box5, text = "Import English List:")
desc5.pack(padx = 5, pady = 20, side = tk.LEFT)

ent5 = tk.Entry(box5, textvariable = ent5_var, width = 40)
ent5.pack(padx = 4, pady = 20,
          side = tk.LEFT)

button5a = tk.Button(box5, text = '...',
                   command = method5a)
button5a.pack(padx = 3, pady = 3, side = tk.LEFT)

button5b = tk.Button(box5, text = 'Submit',
                   command = method5b)
button5b.pack(padx = 3, pady = 3, side = tk.LEFT)


# %% main loop
mainframe.mainloop()




