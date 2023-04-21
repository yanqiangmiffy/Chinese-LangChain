#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: create_knowledge.py
@time: 2023/04/18
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: - emoji：https://emojixd.com/pocket/science
"""
import os
import pandas as pd
from langchain.schema import Document
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from tqdm import tqdm
# 中文Wikipedia数据导入示例：
embedding_model_name = '/root/pretrained_models/text2vec-large-chinese'
docs_path = '/root/GoMall/Knowledge-ChatGLM/cache/financial_research_reports'
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)


# Wikipedia数据处理

# docs = []

# with open('docs/zh_wikipedia/zhwiki.sim.utf8', 'r', encoding='utf-8') as f:
#     for idx, line in tqdm(enumerate(f.readlines())):
#         metadata = {"source": f'doc_id_{idx}'}
#         docs.append(Document(page_content=line.strip(), metadata=metadata))
#
# vector_store = FAISS.from_documents(docs, embeddings)
# vector_store.save_local('cache/zh_wikipedia/')



# docs = []
#
# with open('cache/zh_wikipedia/wiki.zh-sim-cleaned.txt', 'r', encoding='utf-8') as f:
#     for idx, line in tqdm(enumerate(f.readlines())):
#         metadata = {"source": f'doc_id_{idx}'}
#         docs.append(Document(page_content=line.strip(), metadata=metadata))
#
# vector_store = FAISS.from_documents(docs, embeddings)
# vector_store.save_local('cache/zh_wikipedia/')


# 金融研报数据处理
docs = []

for doc in tqdm(os.listdir(docs_path)):
    if doc.endswith('.txt'):
        # print(doc)
        # loader = UnstructuredFileLoader(f'{docs_path}/{doc}', mode="elements")
        # doc = loader.load()
        f=open(f'{docs_path}/{doc}','r',encoding='utf-8')

        # docs.extend(doc)
        docs.append(Document(page_content=''.join(f.read().split()), metadata={"source": f'doc_id_{doc}'}))
vector_store = FAISS.from_documents(docs, embeddings)
vector_store.save_local('cache/financial_research_reports')


# # 英雄联盟
#
# docs = []
#
# lol_df = pd.read_csv('cache/lol/champions.csv')
# # lol_df.columns = ['id', '英雄简称', '英雄全称', '出生地', '人物属性', '英雄类别', '英雄故事']
# print(lol_df)
#
# for idx, row in lol_df.iterrows():
#     metadata = {"source": f'doc_id_{idx}'}
#     text = ' '.join(row.values)
#     # for col in ['英雄简称', '英雄全称', '出生地', '人物属性', '英雄类别', '英雄故事']:
#     #     text += row[col]
#     docs.append(Document(page_content=text, metadata=metadata))
#
# vector_store = FAISS.from_documents(docs, embeddings)
# vector_store.save_local('cache/lol/')
