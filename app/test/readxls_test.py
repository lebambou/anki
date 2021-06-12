import pandas as pd
import numpy as np

file_loc = r"C:\Users\npnew\OneDrive\Documents\dev\k2w2a\app\data\Manulex.xls"
df = pd.read_excel(file_loc, index_col=None, na_values=[''], usecols = "A,R")


for index, row in df.iterrows():
    print(row['LEMMAS'], row['G1-5 U'])
