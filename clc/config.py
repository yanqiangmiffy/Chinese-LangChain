#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: config.py
@time: 2023/04/17
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""


class LangChainCFG:
    llm_model_name = 'THUDM/chatglm-6b-int4-qe'  # 本地模型文件 or huggingface远程仓库
    embedding_model_name = 'GanymedeNil/text2vec-large-chinese'  # 检索模型文件 or huggingface远程仓库
    vector_store_path = '.'
    docs_path = './docs'
