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
    llm_model_name = 'chatglm-6b'  # 本地模型文件 or huggingface远程仓库
    embedding_model_name = 'text2vec-large-chinese'  # 检索模型文件 or huggingface远程仓库
    vector_store_path = '.'
    docs_path = './docs'
