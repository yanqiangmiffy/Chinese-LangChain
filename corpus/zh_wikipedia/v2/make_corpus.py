#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: make_corpus.py
@time: 2023/05/19
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""

import json
import os

from zhconv import convert
from tqdm import tqdm
basedir = '/home/searchgpt/yq/Knowledge-ChatGLM/cache/zh_wikipedia/zhwiki-20230401/AA'
corpus_file = open('/home/searchgpt/yq/Knowledge-ChatGLM/cache/zh_wikipedia/corpus.txt', 'w', encoding='utf-8')
cnt = 0
for wiki_doc in tqdm(os.listdir(basedir)):
    with open(os.path.join(basedir, wiki_doc), 'r', encoding='utf-8') as f:
        for line in tqdm(f,leave=False,desc=""):
            # print(line)
            data = json.loads(line.strip())
            data['title'] = convert(data['title'], 'zh-cn')
            data['text'] = convert(data['text'], 'zh-cn')
            # print(data)
            text = data['title'] + ' ' + data['text']
            corpus_file.write(''.join(text.split('\n')) + '\n')
            cnt += 1
print("文档个数：{}".format(cnt))
# 文档个数：2521667
corpus_file.close()
