import os

from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

embedding_model_name = '/home/searchgpt/pretrained_models/ernie-gram-zh'
docs_path = '/home/searchgpt/yq/Knowledge-ChatGLM/docs'
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

docs = []

for doc in os.listdir(docs_path):
    if doc.endswith('.txt'):
        print(doc)
        loader = UnstructuredFileLoader(f'{docs_path}/{doc}', mode="elements")
        doc = loader.load()
        docs.extend(doc)

vector_store = FAISS.from_documents(docs, embeddings)
vector_store.save_local('vector_store_local')
search_result = vector_store.similarity_search_with_score(query='科比', k=2)
print(search_result)

loader = UnstructuredFileLoader(f'{docs_path}/added/马保国.txt', mode="elements")
doc = loader.load()
vector_store.add_documents(doc)
print(doc)
search_result = vector_store.similarity_search_with_score(query='科比·布莱恩特', k=2)
print(search_result)

"""
[(Document(page_content='王治郅，1977年7月8日出生于北京，前中国篮球运动员，司职大前锋/中锋，现已退役。 [1]', metadata={'source': 'docs/王治郅.txt', 'filename': 'docs/王治郅.txt', 'category': 'Title'}), 285.40765), (Document(page_content='王治郅是中国篮球界进入NBA的第一人，被评选为中国篮坛50大杰出人物和中国申办奥运特使。他和姚明、蒙克·巴特尔一起，被称为篮球场上的“移动长城”。 [5]', metadata={'source': 'docs/王治郅.txt', 'filename': 'docs/王治郅.txt', 'category': 'NarrativeText'}), 290.19086)]
[Document(page_content='科比·布莱恩特（Kobe Bryant，1978年8月23日—2020年1月26日），全名科比·比恩·布莱恩特·考克斯（Kobe Bean Bryant Cox），出生于美国宾夕法尼亚州费城，美国已故篮球运动员，司职得分后卫/小前锋。 [5]  [24]  [84]', metadata={'source': 'docs/added/科比.txt', 'filename': 'docs/added/科比.txt', 'category': 'NarrativeText'}), Document(page_content='1996年NBA选秀，科比于第1轮第13顺位被夏洛特黄蜂队选中并被交易至洛杉矶湖人队，整个NBA生涯都效力于洛杉矶湖人队；共获得5次NBA总冠军、1次NBA常规赛MVP、2次NBA总决赛MVP、4次NBA全明星赛MVP、2次NBA赛季得分王；共入选NBA全明星首发阵容18次、NBA最佳阵容15次（其中一阵11次、二阵2次、三阵2次）、NBA最佳防守阵容12次（其中一阵9次、二阵3次）。 [9]  [24]', metadata={'source': 'docs/added/科比.txt', 'filename': 'docs/added/科比.txt', 'category': 'Title'}), Document(page_content='2007年，科比首次入选美国国家男子篮球队，后帮助美国队夺得2007年美洲男篮锦标赛金牌、2008年北京奥运会男子篮球金牌以及2012年伦敦奥运会男子篮球金牌。 [91]', metadata={'source': 'docs/added/科比.txt', 'filename': 'docs/added/科比.txt', 'category': 'Title'}), Document(page_content='2015年11月30日，科比发文宣布将在赛季结束后退役。 [100]  2017年12月19日，湖人队为科比举行球衣退役仪式。 [22]  2020年4月5日，科比入选奈·史密斯篮球名人纪念堂。 [7]', metadata={'source': 'docs/added/科比.txt', 'filename': 'docs/added/科比.txt', 'category': 'Title'}), Document(page_content='美国时间2020年1月26日（北京时间2020年1月27日），科比因直升机事故遇难，享年41岁。 [23]', metadata={'source': 'docs/added/科比.txt', 'filename': 'docs/added/科比.txt', 'category': 'Title'})]
[(Document(page_content='科比·布莱恩特（Kobe Bryant，1978年8月23日—2020年1月26日），全名科比·比恩·布莱恩特·考克斯（Kobe Bean Bryant Cox），出生于美国宾夕法尼亚州费城，美国已故篮球运动员，司职得分后卫/小前锋。 [5]  [24]  [84]', metadata={'source': 'docs/added/科比.txt', 'filename': 'docs/added/科比.txt', 'category': 'NarrativeText'}), 179.68744), (Document(page_content='2015年11月30日，科比发文宣布将在赛季结束后退役。 [100]  2017年12月19日，湖人队为科比举行球衣退役仪式。 [22]  2020年4月5日，科比入选奈·史密斯篮球名人纪念堂。 [7]', metadata={'source': 'docs/added/科比.txt', 'filename': 'docs/added/科比.txt', 'category': 'Title'}), 200.57565)]
"""