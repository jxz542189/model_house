import os
import pickle
import pandas as pd
import numpy as np

#将address_library.csv转化成txt和pickle
# sentences=[]
# doc = '../data/address_library.csv'
# train = pd.read_csv(doc,encoding='utf-8')
# train_list = np.array(train['Name']).tolist()
# train_list.extend(np.array(train['ShortName']).tolist())
# train_list = list(set(train_list))
# train_list.remove(' ')

# result_path='../data/dic.txt'
# with open(result_path,'w',encoding='utf-8') as fr:
#     for line in train_list:
#         fr.write(line + '\n')

path = '../data/dic.txt'
train_list = []
with open(path,'r',encoding='utf-8') as fr:
    for line in fr.readlines():
        d=line.replace('\n','')
        train_list.append(d)
pickle_path = '../data/address.pkl'
with open(pickle_path, 'wb') as f:
    pickle.dump(train_list, f)