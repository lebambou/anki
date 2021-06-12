
import pandas as pd
import numpy as np
from numpy.random import randn

n_variants = 10
n_defs = 30
n_sents = 10
n_pics = 6
n_fields = 23

stems = np.array(['a'] * n_variants)
stems_b = np.array(['b'] * n_variants)
total = np.array([x for x in range(0, n_variants)])

fields = np.array([
    'word', 'freq', 'audio', 'pos', 'nsm', 'nms-ipa', 'nmpl', 'nmpl-ipa',
    'nfs', 'nfs-ipa', 'nfpl', 'nfpl-ipa', 'adjm', 'adjm-ipa', 'adjf',
    'adjf-ipa', 'defs', 'syns', 'ants', 'hypers', 'hypos', 'derivs', 'pics'
])


defs = np.array(['def' + str(x) for x in range(0, n_defs)])
strs = np.array(['str' + str(x) for x in range(0, n_sents)])
pics = np.array(['pic' + str(x) for x in range(0, n_pics)])


my_multi = pd.DataFrame(index=[stems, total], columns=fields)
my_multi_b = pd.DataFrame(index=[stems_b, total], columns=fields)

my_multi.loc[('a', 3), :] = randn(1, 23)
my_multi.loc[('a', 1), 'word'] = 'botte'


print(my_multi)
print(my_multi_b)

empty = pd.DataFrame()

my_multi = pd.concat([my_multi, empty], axis=0)

print(my_multi)
