from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# 中文Wikipedia数据导入示例：
embedding_model_name = 'GanymedeNil/text2vec-large-chinese'
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
print(embeddings)

vector_store = FAISS.load_local("cache/financial_research_reports", embeddings)
print(vector_store)
res = vector_store.similarity_search_with_score('老窖')
print(res)
