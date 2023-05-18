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

import os

pwd = os.path.dirname(os.path.abspath(__file__))

# 修改成自己的配置！！！
class LangChainCFG:
    llm_model_name = 'THUDM/chatglm-6b-int4-qe'  # 本地模型文件 or huggingface远程仓库
    embedding_model_name = 'GanymedeNil/text2vec-large-chinese'  # 检索模型文件 or huggingface远程仓库
    vector_store_path = os.path.join(pwd, 'cache')
    docs_path = os.path.join(pwd, 'docs')
    kg_vector_stores = {
        '中文维基百科': os.path.join(pwd, 'cache/zh_wikipedia'),
        '大规模金融研报': os.path.join(pwd, 'cache/financial_research_reports'),
        '初始化': os.path.join(pwd, 'cache'),
    }  # 可以替换成自己的知识库，如果没有需要设置为None
    # kg_vector_stores=None
    patterns = ['模型问答', '知识库问答']  #
    n_gpus=1
