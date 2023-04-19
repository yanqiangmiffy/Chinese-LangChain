#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: clean_corpus.py.py
@time: 2023/04/19
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""
"""
    FILE :  clean_corpus.py
    FUNCTION : None
"""
import sys
import os
from optparse import OptionParser


class Clean(object):
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.corpus = []
        self.remove_corpus = []
        self.read(self.infile)
        self.remove(self.corpus)
        self.write(self.remove_corpus, self.outfile)

    def read(self, path):
        print("reading now......")
        if os.path.isfile(path) is False:
            print("path is not a file")
            exit()
        now_line = 0
        with open(path, encoding="UTF-8") as f:
            for line in f:
                now_line += 1
                line = line.replace("\n", "").replace("\t", "")
                self.corpus.append(line)
        print("read finished.")

    def remove(self, list):
        print("removing now......")
        for line in list:
            re_list = []
            for word in line:
                if self.is_chinese(word) is False:
                    continue
                re_list.append(word)
            self.remove_corpus.append("".join(re_list))
        print("remove finished.")

    def write(self, list, path):
        print("writing now......")
        if os.path.exists(path):
            os.remove(path)
        file = open(path, encoding="UTF-8", mode="w")
        for line in list:
            file.writelines(line + "\n")
        file.close()
        print("writing finished")

    def is_chinese(self, uchar):
        """判断一个unicode是否是汉字"""
        if (uchar >= u'\u4e00') and (uchar <= u'\u9fa5'):
            return True
        else:
            return False


if __name__ == "__main__":
    print("clean corpus")

    parser = OptionParser()
    parser.add_option("--input", dest="input", default="", help="input file")
    parser.add_option("--output", dest="output", default="", help="output file")
    (options, args) = parser.parse_args()

    input = options.input
    output = options.output

    try:
        Clean(infile=input, outfile=output)
        print("All Finished.")
    except Exception as err:
        print(err)