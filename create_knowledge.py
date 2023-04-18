#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: create_knowledge.py
@time: 2023/04/18
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""
from langchain.docstore.document import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from tqdm import tqdm

# 中文Wikipedia数据导入示例：
embedding_model_name = '/home/searchgpt/pretrained_models/ernie-gram-zh'
docs_path = '/home/searchgpt/yq/Knowledge-ChatGLM/docs'
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

docs = []

with open('docs/zh_wikipedia/zhwiki.sim.utf8', 'r', encoding='utf-8') as f:
    for idx, line in tqdm(enumerate(f.readlines())):
        metadata = {"source": f'doc_id_{idx}'}
        docs.append(Document(page_content=line.strip(), metadata=metadata))

vector_store = FAISS.from_documents(docs, embeddings)
vector_store.save_local('cache/zh_wikipedia/')
