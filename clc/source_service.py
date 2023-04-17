#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: search.py
@time: 2023/04/17
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""

import os

from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


class SourceService(object):
    def __init__(self, config):
        self.config = config
        self.embeddings = HuggingFaceEmbeddings(model_name=self.config.embedding_model_name)
        self.docs_path = self.config.docs_path
        self.vector_store_path = self.config.vector_store_path

    def init_source_vector(self):
        """
        初始化本地知识库向量
        :return:
        """
        docs = []
        for doc in os.listdir(self.docs_path):
            if doc.endswith('.txt'):
                print(doc)
                loader = UnstructuredFileLoader(f'{self.docs_path}/{doc}', mode="elements")
                doc = loader.load()
                docs.extend(doc)
        self.vector_store = FAISS.from_documents(docs, self.embeddings)
        self.vector_store.save_local(self.vector_store_path)

    def add_document(self, document_path):
        loader = UnstructuredFileLoader(document_path, mode="elements")
        doc = loader.load()
        self.vector_store.add_documents(doc)
        self.vector_store.save_local(self.vector_store_path)

    def load_vector_store(self):
        self.vector_store = FAISS.load_local(self.vector_store_path, self.embeddings)
        return self.vector_store

# if __name__ == '__main__':
#     config = LangChainCFG()
#     source_service = SourceService(config)
#     source_service.init_source_vector()
#     search_result = source_service.vector_store.similarity_search_with_score('科比')
#     print(search_result)
#
#     source_service.add_document('/home/searchgpt/yq/Knowledge-ChatGLM/docs/added/科比.txt')
#     search_result = source_service.vector_store.similarity_search_with_score('科比')
#     print(search_result)
#
#     vector_store=source_service.load_vector_store()
#     search_result = source_service.vector_store.similarity_search_with_score('科比')
#     print(search_result)
