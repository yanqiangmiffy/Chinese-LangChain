#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: chinese_t2s.py.py
@time: 2023/04/19
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""
import sys
import os
import opencc
from optparse import OptionParser


class T2S(object):
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.cc = opencc.OpenCC('t2s')
        self.t_corpus = []
        self.s_corpus = []
        self.read(self.infile)
        self.t2s()
        self.write(self.s_corpus, self.outfile)

    def read(self, path):
        print(path)
        if os.path.isfile(path) is False:
            print("path is not a file")
            exit()
        now_line = 0
        with open(path, encoding="UTF-8") as f:
            for line in f:
                now_line += 1
                line = line.replace("\n", "").replace("\t", "")
                self.t_corpus.append(line)
        print("read finished")

    def t2s(self):
        now_line = 0
        all_line = len(self.t_corpus)
        for line in self.t_corpus:
            now_line += 1
            if now_line % 1000 == 0:
                sys.stdout.write("\rhandling with the {} line, all {} lines.".format(now_line, all_line))
            self.s_corpus.append(self.cc.convert(line))
        sys.stdout.write("\rhandling with the {} line, all {} lines.".format(now_line, all_line))
        print("\nhandling finished")

    def write(self, list, path):
        print("writing now......")
        if os.path.exists(path):
            os.remove(path)
        file = open(path, encoding="UTF-8", mode="w")
        for line in list:
            file.writelines(line + "\n")
        file.close()
        print("writing finished.")


if __name__ == "__main__":
    print("Traditional Chinese to Simplified Chinese")
    # input = "./wiki_zh_10.txt"
    # output = "wiki_zh_10_sim.txt"
    # T2S(infile=input, outfile=output)

    parser = OptionParser()
    parser.add_option("--input", dest="input", default="", help="traditional file")
    parser.add_option("--output", dest="output", default="", help="simplified file")
    (options, args) = parser.parse_args()

    input = options.input
    output = options.output

    try:
        T2S(infile=input, outfile=output)
        print("All Finished.")
    except Exception as err:
        print(err)