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

from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from tqdm import tqdm
# 中文Wikipedia数据导入示例：
embedding_model_name = '/root/pretrained_models/text2vec-large-chinese'
docs_path = '/root/GoMall/Knowledge-ChatGLM/cache/financial_research_reports'
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

# docs = []

# with open('docs/zh_wikipedia/zhwiki.sim.utf8', 'r', encoding='utf-8') as f:
#     for idx, line in tqdm(enumerate(f.readlines())):
#         metadata = {"source": f'doc_id_{idx}'}
#         docs.append(Document(page_content=line.strip(), metadata=metadata))
#
# vector_store = FAISS.from_documents(docs, embeddings)
# vector_store.save_local('cache/zh_wikipedia/')

docs = []

for doc in tqdm(os.listdir(docs_path)):
    if doc.endswith('.txt'):
        # print(doc)
        loader = UnstructuredFileLoader(f'{docs_path}/{doc}', mode="elements")
        doc = loader.load()
        docs.extend(doc)
vector_store = FAISS.from_documents(docs, embeddings)
vector_store.save_local('cache/financial_research_reports')
