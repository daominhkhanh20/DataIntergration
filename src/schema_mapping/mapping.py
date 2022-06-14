import os
import pandas as pd
from valentine import valentine_match, valentine_metrics
from valentine.algorithms import Coma,Cupid,DistributionBased,JaccardLevenMatcher,SimilarityFlooding
from tqdm import tqdm
import pickle

import nltk
nltk.download('omw-1.4')

from pymongo import MongoClient
client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['ProcessData']

colections_name = ['hanoicmp', 'anphat', 'nguyenkim', 'nguyen_cong', 'cellphones', 'laptopworld', 'phucanh']

#load data
data = {}
for col_name in tqdm(colections_name):
    df = []
    data_collections =  database[col_name]
    for item in data_collections.find():
        if col_name == 'cellphones' and item['device'] =='phone':
            continue
        item['web'] = col_name
        df.append(item)
    data[col_name] = pd.DataFrame(df)

# data info
for item in data.values():
    print(item.shape)

# drop null columns when column has more 80% null
for col_name in colections_name:
    drop_colms = []
    size = data[col_name].shape[0]
    for key,value in zip(data[col_name].columns,data[col_name].isna().sum().values):
        if value >= size *0.8:
            drop_colms.append(key)
    drop_colms.append('_id')
    data[col_name].drop(columns=drop_colms,inplace=True)

# data infor after drop
for item in data.values():
    print(item.shape)

# lower all value
for col_name in colections_name:
    for cols in data[col_name].columns:
        data[col_name][cols] = data[col_name][cols].str.lower()


def getPrice(txt):
    target = ''
    if type(txt) is str:

        for s in txt:
            if s.isdigit():
                target += s
    return target

# price standard
for col_name in colections_name:
    data[col_name]['price'] = data[col_name]['price'].apply(lambda txt: getPrice(txt))


def married_matching(matches):
    ap_check = {}
    hn_match = []
    ap_match = []
    dict_match = {}
    for key,value in zip(list(matches.keys()),list(matches.values())):
        # print(key[0][1],key[1][1])
        if key[1][1] not in ap_check.keys() and  key[0][1] not in dict_match.values():
            ap_check[key[1][1]] = 1
            dict_match[key[1][1]] = key[0][1]
            hn_match.append(key[0][1])
            ap_match.append(key[1][1])
    # return_dict = {k:v for k,v in zip(dict_match.values(),dict_match.keys())}
    return dict_match


# match schema
matcher = JaccardLevenMatcher()
match_all = []
for i in range(1,len(colections_name)):
    matches = valentine_match(data[colections_name[0]], data[colections_name[i]], matcher)
    match_all.append(married_matching(matches))

for item in data.values():
    print(item.shape[1])

# columns match with hanoicmp's columns
for item in match_all:
    print(len(item))

# dump match_all info
with open('match_all.pkl','wb') as f:
    pickle.dump(match_all,f)

# remame follwing hanoicmp's columns
for i in range(1,len(data)):
    data[colections_name[i]].rename(columns = match_all[i-1],inplace=True)

# put data to database
def put_data(data):
    for id,item in data.iterrows():
        data_collections.insert_one(item.to_dict())

database = client['ProcessData']

data_collections = database['data_mapping']

max_col_match = 0
for i in range(1,len(data)):
    col_math = set(data[colections_name[0]].columns).intersection(data[colections_name[i]].columns)
    if max_col_match < len(col_math):
        max_col_match = len(col_math)
        cols_1 = col_math
    print(f'Data: {i}',len(col_math))
    put_data(data[colections_name[i]][col_math])
put_data(data[colections_name[0]][cols_1])