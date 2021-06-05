# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:35:32 2021

@author: npnew
"""

from tkinter import *
root = Tk()

Label(text="Position 1", width=10).grid(row=0, column=0)
Label(text="Position 2", width=10).grid(row=0, column=1)
Label(text="Position 3", width=10).grid(row=1, column=0)
Label(text="Position 4", width=10).grid(row=1, column=1)
root.mainloop()