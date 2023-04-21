#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: model.py
@time: 2023/04/17
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""
from langchain.chains import RetrievalQA
from langchain.prompts.prompt import PromptTemplate

from clc.config import LangChainCFG
from clc.gpt_service import ChatGLMService
from clc.source_service import SourceService


class LangChainApplication(object):
    def __init__(self, config):
        self.config = config
        self.llm_service = ChatGLMService()
        self.llm_service.load_model(model_name_or_path=self.config.llm_model_name)
        # self.llm_service.load_model_on_gpus(model_name_or_path=self.config.llm_model_name,num_gpus=self.config.n_gpus)
        self.source_service = SourceService(config)

        # if self.config.kg_vector_stores is None:
        #     print("init a source vector store")
        #     self.source_service.init_source_vector()
        # else:
        #     print("load zh_wikipedia source vector store ")
        #     try:
        #         self.source_service.load_vector_store(self.config.kg_vector_stores['初始化知识库'])
        #     except Exception as e:
        #         self.source_service.init_source_vector()

    def get_knowledge_based_answer(self, query,
                                   history_len=5,
                                   temperature=0.1,
                                   top_p=0.9,
                                   top_k=4,
                                   web_content='',
                                   chat_history=[]):
        if web_content:
            prompt_template = f"""基于以下已知信息，简洁和专业的来回答用户的问题。
                                如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分，答案请使用中文。
                                已知网络检索内容：{web_content}""" + """
                                已知内容:
                                {context}
                                问题:
                                {question}"""
        else:
            prompt_template = """基于以下已知信息，简洁和专业的来回答用户的问题。
                                            如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分，答案请使用中文。
                                            已知内容:
                                            {context}
                                            问题:
                                            {question}"""
        prompt = PromptTemplate(template=prompt_template,
                                input_variables=["context", "question"])
        self.llm_service.history = chat_history[-history_len:] if history_len > 0 else []

        self.llm_service.temperature = temperature
        self.llm_service.top_p = top_p

        knowledge_chain = RetrievalQA.from_llm(
            llm=self.llm_service,
            retriever=self.source_service.vector_store.as_retriever(
                search_kwargs={"k": top_k}),
            prompt=prompt)
        knowledge_chain.combine_documents_chain.document_prompt = PromptTemplate(
            input_variables=["page_content"], template="{page_content}")

        knowledge_chain.return_source_documents = True

        result = knowledge_chain({"query": query})
        return result

    def get_llm_answer(self, query='', web_content=''):
        if web_content:
            prompt = f'基于网络检索内容：{web_content}，回答以下问题{query}'
        else:
            prompt = query
        result = self.llm_service._call(prompt)
        return result


if __name__ == '__main__':
    config = LangChainCFG()
    application = LangChainApplication(config)
    # result = application.get_knowledge_based_answer('马保国是谁')
    # print(result)
    # application.source_service.add_document('/home/searchgpt/yq/Knowledge-ChatGLM/docs/added/马保国.txt')
    # result = application.get_knowledge_based_answer('马保国是谁')
    # print(result)
    result = application.get_llm_answer('马保国是谁')
    print(result)
