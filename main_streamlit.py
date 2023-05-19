import os
import shutil
from app_modules.overwrites import postprocess
from app_modules.presets import *
from clc.langchain_application import LangChainApplication
import streamlit as st
from streamlit_chat import message as message_chat

MAX_TURNS = 20
MAX_BOXES = MAX_TURNS * 2

st.set_page_config(page_title='Chinese-LangChain', layout='wide', initial_sidebar_state='auto')

# 修改成自己的配置！！！
class LangChainCFG:
    llm_model_name = 'THUDM/chatglm-6b-int4-qe'  # 本地模型文件 or huggingface远程仓库
    # llm_model_name = 'THUDM/chatglm-6b'  # 本地模型文件 or huggingface远程仓库
    embedding_model_name = 'GanymedeNil/text2vec-large-chinese'  # 检索模型文件 or huggingface远程仓库
    vector_store_path = './cache'
    docs_path = './docs'
    kg_vector_stores = {
        '默认知识库': './cache',
        '中文维基百科': './cache/zh_wikipedia',
        '大规模金融研报': './cache/financial_research_reports',        
    }  # 可以替换成自己的知识库，如果没有需要设置为None
    # kg_vector_stores=None
    patterns = ['模型问答', '知识库问答']  #
    n_gpus=1
    # 请输入GOOLGE SERPER API KEY，免费账号申请地址：https://serper.dev/
    serper_api_key = "8102810aa7731f849ecb415acc225a51f906c66f"
    # 对搜索结果分析的词向量文件
    em_data_dir = "/root/emdata/"

def get_file_list():
    if not os.path.exists("docs"):
        return []
    return [f for f in os.listdir("docs")]

@st.cache_resource
def init_application():
    config = LangChainCFG()
    application = LangChainApplication(config)
    application.source_service.init_source_vector()
    file_list = get_file_list()
    print("=========================== 😃 Enjoy your journey and be lucky! =========================================")
    print("\n")
    return config, application, file_list

if "application" not in st.session_state:
    st.session_state.config, st.session_state.application, st.session_state.file_list = init_application()

def upload_file(file):
    if not os.path.exists("docs"):
        os.mkdir("docs")
    file_list = st.session_state.file_list
    application = st.session_state.application
    filename = os.path.basename(file.name)
    shutil.move(file.name, "docs/" + filename)
    # file_list首位插入新上传的文件
    file_list.insert(0, filename)
    application.source_service.add_document("docs/" + filename)
    return gr.Dropdown.update(choices=file_list, value=filename)

def set_knowledge(kg_name, history):
    config = st.session_state.config
    application = st.session_state.application
    try:
        application.source_service.load_vector_store(config.kg_vector_stores[kg_name])
        msg_status = f'{kg_name}知识库已成功加载'
    except Exception as e:
        print(e)
        msg_status = f'{kg_name}知识库未成功加载'
    return history + [[None, msg_status]]

def clear_session():
    st.session_state['gpt_history'] = []
    st.session_state['human_history'] = []  

def predict(input,
            large_language_model,
            embedding_model,
            top_k,
            use_web,
            use_pattern,
            history=None):
    # print(large_language_model, embedding_model)
    print('\n-------------------------------------------------')
    print(input)
    print('-------------------------------------------------')
    if history == None:
        history = []
    application = st.session_state.application

    if use_web == '使用':
        web_content = application.source_service.search_web(query=input)
    else:
        web_content = ''
    search_text = ''
    result = ''

    # with container:
    #     message_chat(input, avatar_style="big-smile", key=str(len(history)) + "_user")                                

    if use_pattern == '模型问答':        
        gen = application.get_llm_answer(query=input, web_content=web_content, history=history, use_stream=1)
        search_text = web_content   
        try:                 
            st.write("AI正在回复:")
            with st.empty():
                while True:
                    try:
                        result = next(gen)  # 获取下一个数据
                        history = application.llm_service.history
                        _, response = history[-1] 
                        st.write(response)
                    except StopIteration:  # 当所有的数据都被遍历完，next函数会抛出StopIteration的异常
                        st.session_state['human_history'].append((input, response))
                        # 完成后打印最终的回答
                        history = application.llm_service.history                        
                        _, response = history[-1]
                        print('--------------- LLM Final Answer ----------------')
                        print(response)
                        break
        except KeyboardInterrupt:
            print("\nCtrl+C is pressed...")

        return '', history, history, search_text

    else:
        resp = application.get_knowledge_based_answer(
            query=input,
            history_len=1,
            temperature=0.1,
            top_p=0.9,
            top_k=top_k,
            web_content=web_content,
            chat_history=history
        )

        st.write("AI正在回复:")
        st.write(resp['result'])
        print('--------------- LLM Final Answer ----------------')
        print(resp['result'])
        st.session_state['human_history'].append((input, resp['result']))

        # history.append((input, resp['result']))
        history = application.llm_service.history

        for idx, source in enumerate(resp['source_documents'][:4]):
            sep = f'----------【知识库搜索结果{idx + 1}：】---------------\n'
            search_text += f'{sep}\n{source.page_content}\n\n'
        print(search_text)
        search_text += "----------【网络检索内容】-----------\n"
        search_text += web_content
        return '', history, history, search_text


# 在这里读取CSS文件并使用st.markdown来设置样式可能不会成功，因为Streamlit的安全策略可能会阻止内联CSS

st.title("Chinese-LangChain")

embedding_model = st.sidebar.selectbox("Embedding model", ["text2vec-base"], 0)

large_language_model = st.sidebar.selectbox("large language model", ["ChatGLM-6B"], 0)

top_k = st.sidebar.slider("检索top-k文档", 1, 20, 4, 1)

use_web = st.sidebar.radio("web search", ["使用", "不使用"], 1)

use_pattern = st.sidebar.radio("模式", ['模型问答', '知识库问答'], 0)

kg_name = st.sidebar.radio("知识库", list(st.session_state.config.kg_vector_stores.keys()), 0)

if st.sidebar.button("加载知识库"):
    set_knowledge(kg_name)
    st.success("知识库已加载")

uploaded_file = st.sidebar.file_uploader("将文件上传到知识库，内容要尽量匹配", type=['.txt', '.md', '.docx', '.pdf'])

if uploaded_file is not None:
    upload_file(uploaded_file)
    st.success("文件已上传")

# 模型看到的对话历史{prompt, response}
if 'gpt_history' not in st.session_state:
    st.session_state['gpt_history'] = []

# 人看到的对话历史{query, response}
if 'human_history' not in st.session_state:
    st.session_state['human_history'] = []    

container = st.container()
message = st.text_input('请输入问题')

# 创建两列
col1, col2 = st.columns(2)

# 在每列中添加一个按钮
send_button = col1.button('🚀   发 送    ')
clear_button = col2.button('🧹 清除历史对话')

if "clear_clicked" not in st.session_state:
    st.session_state["clear_clicked"] = False

if clear_button or st.session_state["clear_clicked"]:
    st.success("历史对话已清除")
    clear_session()    
    st.session_state["clear_clicked"] = False

# 显示历史对话内容
with container:
    human_history = st.session_state['human_history']
    if len(human_history) > 0:
        if len(human_history) > MAX_BOXES:
            human_history = human_history[-MAX_TURNS:]
        for i, (query, response) in enumerate(human_history):
            message_chat(query, avatar_style="big-smile", key=str(i) + "_user")
            message_chat(response, avatar_style="bottts", key=str(i))

# 点击发送按钮，暂不处理输入回车
if send_button:
    _, _, history, search_result = predict(message, large_language_model, embedding_model, top_k, use_web, use_pattern, st.session_state["gpt_history"])                
    st.session_state["gpt_history"] = history
    st.text_area('搜索结果', search_result, height=200)      

st.markdown("""提醒：<br>
            [Chinese-LangChain](https://github.com/yanqiangmiffy/Chinese-LangChain) <br>
            有任何使用问题[Github Issue区](https://github.com/yanqiangmiffy/Chinese-LangChain)进行反馈. <br>
            """, unsafe_allow_html=True)


