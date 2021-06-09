
import pandas as pd
import numpy as np
from numpy.random import randn


stems = np.array(['a', 'a', 'a', 'a', 'a', 'a'])
total = np.array([x for x in range(0, 6)])

fields = np.array([
    'word', 'freq', 'audio', 'pos', 'nsm', 'nms-ipa', 'nmpl', 'nmpl-ipa',
    'nfs', 'nfs-ipa', 'nfpl', 'nfpl-ipa', 'adjm', 'adjm-ipa', 'adjf',
    'adjf-ipa', 'defs', 'syns', 'ants', 'hypers', 'hypos', 'derivs', 'pics'
])
arrays = [
    stems, total
]

defs = np.array(['def' + str(x) for x in range(0, 30)])
strs = np.array(['str' + str(x) for x in range(0, 10)])
pics = np.array(['pic' + str(x) for x in range(0, 5)])

vals = randn(23)

my_df = pd.DataFrame(columns=fields)
my_df.loc[0] = vals
my_df.loc[1] = vals

my_multi = pd.DataFrame(index=arrays, columns=fields)

my_multi.loc[('a', 3), :] = randn(1, 23)
my_multi.loc[('a', 1), 'word'] = 'botte'
my_multi.loc[('a', 0), 'freq'] = [['try', 'it', 'out'], ['yes', 'you', 'can']]

print(my_multi)
