from pymongo import MongoClient
from pymongo.collection import Collection
import pandas as pd
from pandas import DataFrame
from typing import List, Dict
from bson.objectid import ObjectId
from strsimpy.jaccard import Jaccard
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
import re
from collections import Counter, defaultdict
import recordlinkage
from tqdm import tqdm

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)

database = client['ProcessData']


def parser(sent):
    product_name = re.sub('\(.*?\)', '', sent).strip()
    detail = re.findall('\(.*?\)', sent)
    if len(detail) > 0:
        final_detail = []
        for sample in detail:
            sample = sample[1:-1]
            if '|' in sent:
                sample = sample.split('|')
            elif '/' in sent:
                sample = sample.split('/')
            if isinstance(sample, list) and len(sample) > len(final_detail):
                final_detail = sample
        if len(final_detail) > 0:
            final_detail = [ele.strip() for ele in final_detail]
            if len(final_detail) == 1:
                product_name = product_name + " " + final_detail[0]
                final_detail = None
        else:
            final_detail = None
    else:
        final_detail = None
    return product_name, final_detail


def process_df(data: DataFrame):
    data['new_product_name'] = None
    for idx, row in tqdm(data.iterrows(), total=len(data)):
        if pd.isnull(data.loc[idx, 'product_name']) is False:
            if 'macbook' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'apple'
            elif any(brand in row['product_name'].lower() for brand in ['alienware', 'del']):
                data.loc[idx, 'Hãng sản xuất'] = 'dell'
            elif 'hp' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'hp'
            elif 'microsoft' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'microsoft'
            elif 'msi' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'msi'
            elif 'lg' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'lg'
            elif 'acer' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'acer'
            elif 'asus' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'asus'
            elif 'lenovo' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'lenovo'
            elif 'gigabyte' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'gigabyte'
            elif 'huawei' in row['product_name'].lower():
                data.loc[idx, 'Hãng sản xuất'] = 'huawei'
            # else:
            #     print(row['product_name'])

            product_name = row['product_name']
            product_name, detail = parser(product_name)
            data.loc[idx, 'new_product_name'] = product_name
            if detail is not None and len(detail) >= 6:
                data.loc[idx, 'Bộ vi xử lý'] = detail[0]
                data.loc[idx, 'ram'] = detail[1]
                data.loc[idx, 'Ổ cứng'] = detail[2]
                data.loc[idx, 'VGA'] = detail[3]
                data.loc[idx, 'Màn hình'] = detail[4]
                data.loc[idx, 'Hệ điều hành'] = detail[5]
            if detail is not None and len(detail) >= 7:
                data.loc[idx, 'Mầu sắc'] = detail[6]

        if pd.isnull(data.loc[idx, 'ram']) and pd.isnull(data.loc[idx, 'Bộ nhớ trong']) is False:
            words = re.sub('[^a-zA-Z0-9]', " ", data.loc[idx, 'Bộ nhớ trong']).strip().split(" ")
            for word in words:
                if 'gb' in word.lower():
                    data.loc[idx, 'ram'] = word.lower()
                    break
    data['Bộ vi xử lý'] = data['Bộ vi xử lý'].astype(str).apply(lambda x: " ".join(re.findall('\w+', x)))
    return data


class MatchingData:
    def __init__(self, df: List[DataFrame] = None,
                 websites: List = None,
                 source_collection: Collection = None,
                 des_collection: Collection = None,
                 list_ids: List = None,
                 mode_compare_custom: bool = False):
        self.df = df
        self.websites = websites
        self.source_collection = source_collection
        self.des_collection = des_collection
        self.id2group = {}
        self.group2id = defaultdict(list)
        self.group = 0
        self.list_ids = list_ids
        self.web_counter = {key: 0 for key in self.websites}
        self.mode_compare_custom = mode_compare_custom

    @classmethod
    def init_attribute(cls, source_collection: str = 'data_mapping',
                       des_collection: str = 'data_matching2',
                       mode_compare_custom: bool = False):
        source_collection = database[source_collection]
        des_collection = database[des_collection]
        if des_collection.count_documents(filter={}) > 0:
            des_collection.drop()

        documents = []
        for doc in source_collection.find():
            documents.append(doc)
        documents = pd.DataFrame(documents)
        documents = process_df(documents)
        documents = documents[documents['Hãng sản xuất'].notna()].reset_index(drop=True)
        documents[['Hệ điều hành', 'web', 'Bộ vi xử lý', 'Hãng sản xuất', 'Pin', 'product_name', 'new_product_name',
                   'Bộ nhớ trong', 'ram', 'Ổ cứng', 'VGA', 'price', 'Màn hình', 'Mầu sắc']].to_csv('temp.csv',
                                                                                                   index=False)
        websites = list(set(documents['web'].values.tolist()))
        df, list_ids = [], []
        for website in websites:
            df_temp = documents[documents['web'] == website].reset_index(drop=True)
            df.append(df_temp)
            list_ids.extend(df_temp['_id'].values.tolist())

        return cls(df=df, websites=websites, source_collection=source_collection,
                   des_collection=des_collection, list_ids=list_ids, mode_compare_custom=mode_compare_custom)

    def compare_custom(self, index: int, index1: int, threshold: float = 0.7):
        df = self.df[index]
        df1 = self.df[index1]
        list_key = ['new_product_name', 'Ổ cứng', 'ram', 'VGA', 'Bộ vi xử lý']
        weight = [0.5, 0.125, 0.125, 0.125, 0.125]
        jaccard_fn = Jaccard(k=2)
        normalized_levenshtein = NormalizedLevenshtein()
        cnt = 0
        print(f"Start matching custom between {self.websites[index]} and {self.websites[index1]}")
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            for idx1, row1 in df1.iterrows():
                score = 0
                for index_key, key in enumerate(list_key):
                    if key == 'new_product_name':
                        score += weight[index_key] * jaccard_fn.similarity(str(row[key]), str(row1[key]))
                    else:
                        score += weight[index_key] * normalized_levenshtein.similarity(str(row[key]), str(row1[key]))
                if threshold < score < 1:
                    cnt += 1
                    id1 = row['_id']
                    id2 = row1['_id']
                    if id1 in self.list_ids:
                        self.list_ids.remove(id1)

                    if id2 in self.list_ids:
                        self.list_ids.remove(id2)

                    if id1 in self.id2group and id2 not in self.id2group:
                        self.id2group[id2] = self.id2group[id1]
                        self.group2id[self.id2group[id1]].append(id2)
                    elif id2 in self.id2group and id1 not in self.id2group:
                        self.id2group[id1] = self.id2group[id2]
                        self.group2id[self.id2group[id2]].append(id1)
                    elif id1 not in self.id2group and id2 not in self.id2group:
                        self.id2group[id1] = self.group
                        self.id2group[id2] = self.group
                        self.group2id[self.group].extend([id1, id2])
                        self.group += 1

        print(f"Total matching between {self.websites[index]} and {self.websites[index1]} is {cnt}")

    def compare(self, index: int, index1: int):
        print(f"Start matching: {self.websites[index]} and {self.websites[index1]}")
        df = self.df[index]
        df1 = self.df[index1]
        indexer = recordlinkage.Index()
        indexer.full()
        candidates = indexer.index(df, df1)

        compare = recordlinkage.Compare()
        list_keys = {
            'new_product_name': 0.8,
            'Ổ cứng': 0.8,
            'ram': 0.8,
            "VGA": 0.7,
            'Bộ vi xử lý': 0.9,
            'Cân nặng': 0.8
        }
        for feature, threshold in list_keys.items():
            compare.string(feature, feature, threshold=threshold, label=feature)
        features = compare.compute(candidates, df, df1)
        index_accept = []
        for idx, row in features.iterrows():
            if any(row[feature] == 0 for feature in list_keys.keys()):
                continue
            index_accept.append(idx)
        if len(index_accept) > 0:
            temp = features[features.index.isin(index_accept)]
            print(temp.head(10))
        potential_features = features[features.index.isin(index_accept)].reset_index()
        print(f"Total matching: {len(potential_features)}")
        if len(potential_features) > 0:
            for idx, row in potential_features.iterrows():
                id1 = df.loc[row[0]]['_id']
                id2 = df1.loc[row[1]]['_id']
                if id1 in self.list_ids:
                    self.list_ids.remove(id1)

                if id2 in self.list_ids:
                    self.list_ids.remove(id2)

                if id1 in self.id2group and id2 not in self.id2group:
                    self.id2group[id2] = self.id2group[id1]
                    self.group2id[self.id2group[id1]].append(id2)
                elif id2 in self.id2group and id1 not in self.id2group:
                    self.id2group[id1] = self.id2group[id2]
                    self.group2id[self.id2group[id2]].append(id1)
                elif id1 not in self.id2group and id2 not in self.id2group:
                    self.id2group[id1] = self.group
                    self.id2group[id2] = self.group
                    self.group2id[self.group].extend([id1, id2])
                    self.group += 1

    def fit(self):
        print(self.websites)
        if self.mode_compare_custom:
            print("Turn on mode custom mode")
        for i in range(len(self.websites) - 1):
            for j in range(i + 1, len(self.websites)):
                if self.mode_compare_custom:
                    self.compare_custom(i, j, threshold=0.85)
                else:
                    self.compare(i, j)

        print(f"Total: {len(self.list_ids)} not matching")
        cnt = len(self.group2id)
        for id in self.list_ids:
            self.group2id[cnt].append(id)
            cnt += 1

        print("Start insert into database")
        cnt = 0
        for group in tqdm(self.group2id.keys(), total=len(self.group2id.keys())):
            list_ids = self.group2id[group]
            cnt += len(list_ids)
            list_ids = [ObjectId(id) for id in list_ids]
            docs = self.source_collection.find({'_id': {'$in': list_ids}})
            data = {
                'product_name': docs[0]['product_name']
            }
            list_shop = []
            for doc in docs:
                list_shop.append(doc)

            data['information'] = list_shop
            data['count'] = len(list_shop)
            self.des_collection.insert_one(data)

        print(f"Number document compare: {cnt}")


matching = MatchingData.init_attribute(source_collection='schema_mapping1', des_collection='data_matching2v10', mode_compare_custom=True)
matching.fit()
