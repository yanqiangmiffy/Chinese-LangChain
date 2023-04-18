from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# 中文Wikipedia数据导入示例：
embedding_model_name = '/root/pretrained_models/ernie-gram-zh'
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

vector_store = FAISS.load_local("/root/GoMall/Knowledge-ChatGLM/cache/zh_wikipedia", embeddings)
print(vector_store)
res = vector_store.similarity_search_with_score('闫强')
print(res)
