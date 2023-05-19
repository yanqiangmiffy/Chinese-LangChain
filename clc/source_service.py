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
import re
import unicodedata as ucd
import warnings
warnings.filterwarnings('ignore')

import heapq
import time
import pprint

from googleapiclient.discovery import build
import re
import requests
#from HTMLParser import HTMLParser
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc 
import spacy
# 必须导入pytextrank，虽然表面上没用上，
import pytextrank
import nltk
import fasttext
from bs4 import BeautifulSoup
#import fasttext.util
import json
import heapq
import re
import time
from urllib import parse

import requests
from bs4 import BeautifulSoup

from .textrank_utils import top_sentence
from .score_utils import score, score_2, score_3

from duckduckgo_search import ddg
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


class prey(object):
    def __init__(self, value, sentence):
        self.value =  value
        self.sentence = sentence
    # 重写 < 符号用于sorted
    def __lt__(self, other):
        return self.value < other.value
    def __gt__(self, other):
        return self.value > other.value
    def __le__(self, other):
        return self.value <= other.value
    def __eq__(self, other):
        return self.value == other.value
    def __ne__(self, other):
        return self.value != other.value
    def __ge__(self, other):
        return self.value >= other.value

def containenglish(str0):
    import re
    return bool(re.search('[a-z]', str0))


def clean_html(html: str) -> str:
    """Remove HTML markup from the given string."""
    # Remove inline JavaScript/CSS, HTML comments, and HTML tags
    cleaned_html = re.sub(
        r"(?is)<(script|style).*?>.*?(</\1>)|<!--(.*?)-->[\n]?|<(?s).*?>", "", html.strip()
    )

    # Deal with whitespace and HTML entities
    cleaned_html = re.sub(
        r"&nbsp;|  |\t|&.*?;[0-9]*&.*?;|&.*?;", "", cleaned_html
    )

    # Normalize the text
    # cleaned_html = ucd.normalize('NFKC', cleaned_html).replace(' ', '')

    return cleaned_html.strip()

def select(new):
    if len(new) < 10:
        oral = new
    elif len(new) // 10 < 10:
        oral = new[:20]
    elif len(new) // 10 > 50:
        oral = new[:50]
    else:
        oral = new[:len(new) // 10]
    return oral

def get_web_response(url):
    print("[ENGINE] get web response")
    try:
        response = requests.get(url=url, timeout=5)
        response.encoding = 'utf-8'
        return response
    except requests.exceptions.RequestException:
        print("requests post fail")
        return None

def extract_description(soup):
    description = soup.find(attrs={"name": "description"})
    if description:
        content = description.get('content')
        if content:
            return content
    return None

def summ_web(q, url, ft_en, ft_zh, is_eng, nlp_en, nlp_zh, measure_en, measure_zh, snippet,title):
    print(q)
    print(url)
    #start_time = time.time()
    url = parse.unquote(url)

    response = get_web_response(url)
    if response is None:
        return {"title":title, "url": url, "summ": snippet, "note": "fail to get ... use snippet", "type": "snippet"}

    soup = BeautifulSoup(response.text, "html.parser")
    description = extract_description(soup)

    if description:
        if all(key_word in description for key_word in q.split()):
            return {"title":title, "url": url, "summ": description, "note": "use description as summ", "type": "description"}

    text = clean_html(response.text)
    sentences = re.split("\n|。|\.", text)

    ft = ft_en if is_eng else ft_zh
    measure = measure_en if is_eng else measure_zh
    nlp = nlp_en if is_eng else nlp_zh

    scored_sentences = []
    for sentence in sentences:
        if 3 <= len(sentence) <= 200:
            scored_sentence = {
                'ft': -1 * score(q, sentence, ft) if ft else None,
                'score_2': -1 * score_2(q, sentence),
                'measure': -1 * score_3(q, sentence, measure=measure) if measure else None,
                'sentence': sentence
            }
            scored_sentences.append(scored_sentence)

    top_sentences = heapq.nsmallest(5, scored_sentences, key=lambda x: x['ft'] or float('inf')) + \
                    heapq.nsmallest(10, scored_sentences, key=lambda x: x['score_2']) + \
                    heapq.nsmallest(5, scored_sentences, key=lambda x: x['measure'] or float('inf'))

    stop_word = "." if is_eng else "。"
    combined_text = stop_word.join([sentence['sentence'] for sentence in top_sentences])

    if len(combined_text) < 3:
        return {"title":title, "url": url, "summ": snippet, "note": "bad web, fail to summ, use snippet,", "type": "snippet"}

    try:
        summary = top_sentence(text=combined_text, limit=3, nlp=nlp)
        summary = "".join(summary)
    except Exception as e:
        return {"title":title, "url": url, "summ": snippet, "note": "unknown summ error , use snippet", "type": "snippet"}

    if any(key_word in summary for key_word in q.split()):
        return {"title":title, "url": url, "summ": summary, "note": "good summ and use it", "type": "my_summ"}

    return {"title":title, "url": url, "summ": snippet, "note": "poor summ , use snippet", "type": "snippet"}

def search_api(q, SERPER_KEY):
    import requests
    import json
    url = "https://google.serper.dev/search"

    if containenglish(q):
        payload = json.dumps({"q": q,})
    else:
        payload = json.dumps({"q": q})#,"gl": "cn","hl": "zh-cn"})
    headers = {
        'X-API-KEY': SERPER_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_dict = json.loads(response.text)

    return response_dict

def filter_urls(urls, snippets, titles, black_list=None, topk=3):
    if black_list is None:
        black_list = ["enoN, youtube.com, bilibili.com", "zhihu.com"]

    filtered_urls, filtered_snippets, filtered_titles = [], [], []
    count = 0
    for url, snippet, title in zip(urls, snippets, titles):
        if all(domain not in url for domain in black_list) and url.split(".")[-1] != "pdf":
            filtered_urls.append(url)
            filtered_snippets.append(snippet)
            filtered_titles.append(title)
            count += 1
            if count >= topk:
                break

    return filtered_urls, filtered_snippets, filtered_titles

def engine(q, SERPER_KEY,ft_en, ft_zh, nlp_en, nlp_zh, measure_en, measure_zh, topk=3):
    start_time = time.time()
    is_eng = containenglish(q)

    response = search_api(q, SERPER_KEY)

    if "answerBox" in response.keys():
        url = response["answerBox"].get("link", response["organic"][0]["link"])
        summ = response["answerBox"]
        print("[EnGINE] answerBox")
        print("[ENGINE] query cost:", time.time() - start_time)
        return {"url": url, "summ": summ, "note": "directly return answerBox, thx google !", "type": "answerBox"}

    raw_urls = [i["link"] for i in response["organic"]]
    raw_snippets = [i["snippet"] for i in response["organic"]]
    raw_titles = [i["title"] for i in response["organic"]]
    urls, snippets, titles = filter_urls(raw_urls, raw_snippets, raw_titles, topk=topk)

    results = {}
    for i, url in enumerate(urls):
        try:
            summ = summ_web(q, url, ft_en, ft_zh, is_eng, nlp_en, nlp_zh, measure_en, measure_zh, snippets[i], titles[i])
        except:
            summ = {"url": url, "summ": snippets[i], "note": "unbelievable error, use snippet !", "type": "snippet", "title":titles[i]}

        results[str(i)] = summ

    print("[ENGINE] query cost:", time.time() - start_time)
    return results


class SourceService(object):
    def __init__(self, config):
        self.vector_store = None
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

        import time
        self.serper_api_key = self.config.serper_api_key
        print("loading web query embeddings ...")
        self.ft_en = fasttext.load_model(self.config.em_data_dir + 'cc.en.300.bin')
        self.ft_zh = fasttext.load_model(self.config.em_data_dir + 'cc.zh.300.bin')
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_zh = spacy.load("zh_core_web_sm")
        from .score_utils import score_measure
        self.measure_en = None#score_measure("en")
        self.measure_zh = None#score_measure("zh")
        print("web query embeddings loaded ...")


    def add_document(self, document_path):
        loader = UnstructuredFileLoader(document_path, mode="elements")
        doc = loader.load()
        self.vector_store.add_documents(doc)
        self.vector_store.save_local(self.vector_store_path)

    def load_vector_store(self, path):
        if path is None or path == "未选择":
            self.vector_store = FAISS.load_local(self.vector_store_path, self.embeddings)
        else:
            self.vector_store = FAISS.load_local(path, self.embeddings)
        return self.vector_store

    def search_web(self, query):

        # SESSION.proxies = {
        #     "http": f"socks5h://localhost:7890",
        #     "https": f"socks5h://localhost:7890"
        # }
        try:
            # results = ddg(query)        
            results = engine(query, self.serper_api_key, self.ft_en, self.ft_zh, self.nlp_en, self.nlp_zh, self.measure_en, self.measure_zh)
            web_content = ''
            print('web search result:')
            print(str(results))
            '''
            if results:
                for result in results:
                    web_content += result['summ']
            return web_content
            '''
            return str(results)
            
        except Exception as e:
            print(f"网络检索异常:{query}")
            print(e)
            return ''
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
