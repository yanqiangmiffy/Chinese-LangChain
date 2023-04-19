#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: wiki_process.py
@time: 2023/04/19
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: https://blog.csdn.net/weixin_40871455/article/details/88822290
"""
import logging
import sys
from gensim.corpora import WikiCorpus

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)
'''
    extract data from wiki dumps(*articles.xml.bz2) by gensim.
    @2019-3-26
'''


def help():
    print("Usage: python wikipro.py zhwiki-20190320-pages-articles-multistream.xml.bz2 wiki.zh.txt")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        help()
        sys.exit(1)
    logging.info("running %s" % ' '.join(sys.argv))
    inp, outp = sys.argv[1:3]
    i = 0

    output = open(outp, 'w', encoding='utf8')
    wiki = WikiCorpus(inp, dictionary={})
    for text in wiki.get_texts():
        output.write(" ".join(text) + "\n")
        i = i + 1
        if (i % 10000 == 0):
            logging.info("Save " + str(i) + " articles")
    output.close()
    logging.info("Finished saved " + str(i) + "articles")

    # 命令行下运行
    # python wikipro.py cache/zh_wikipedia/zhwiki-latest-pages-articles.xml.bz2 wiki.zh.txt