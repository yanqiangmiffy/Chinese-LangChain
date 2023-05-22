from transformers import AutoModel, AutoTokenizer
import streamlit as st
from PIL import Image
import numpy as np
import tempfile
from streamlit_chat import message as message_chat

def predict(input, image_path, chatbot, max_length, top_p, temperature, history):
    if image_path is None:
        return [(input, "图片为空！请重新上传图片并重试。")]
    for response, history in st.session_state.model.stream_chat(st.session_state.tokenizer, image_path, input, history, max_length=max_length, top_p=top_p,
                                               temperature=temperature):
        yield response, history


@st.cache_resource
def init_application():
    st.session_state['history'] = []
    st.session_state['chatbot'] = []  

    tokenizer = AutoTokenizer.from_pretrained("THUDM/visualglm-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/visualglm-6b", trust_remote_code=True).half().cuda()
    model = model.eval()
    st.session_state.tokenizer = tokenizer
    st.session_state.model = model

def clear_session():
    st.session_state['chatbot'].clear()
    st.session_state['history'].clear()

if "chatbot" not in st.session_state:
    init_application()

st.title('VisualGLM')

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
container = st.container()

user_input = st.text_input('Input...')
max_length = st.sidebar.slider("Maximum length", 0, 4096, 2048, 1)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.4, 0.01)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.8, 0.01)

if uploaded_file is not None:
    # image_path = Image.open(uploaded_file)
    image = Image.open(uploaded_file)
    with container:
        st.image(image, use_column_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
        image.save(temp.name, "PNG")
        image_path = temp.name
        st.session_state.image = image_path

    if "uploaded_file" in st.session_state and st.session_state.uploaded_file != uploaded_file:
        clear_session()
    st.session_state.uploaded_file = uploaded_file
    

# 创建两列
col1, col2 = st.columns(2)
send_button = col1.button('🚀   发 送    ')
clear_button = col2.button('🧹 清除历史对话')

if clear_button:
    clear_session()

if send_button:
    if len(user_input) > 0:
        gen = predict(user_input, st.session_state.image, st.session_state['chatbot'], max_length, top_p, temperature, 
                        st.session_state['history'] if st.session_state['history'] else [])
        while True:
            try:
                response, st.session_state['history'] = next(gen)
            except StopIteration:  # 当所有的数据都被遍历完，next函数会抛出StopIteration的异常
                st.session_state['chatbot'].append((user_input, response))
                break
        user_input = ''

human_history = st.session_state['chatbot']
for i, (query, response) in enumerate(human_history):
    message_chat(query, avatar_style="big-smile", key=str(i) + "_user") # User input
    message_chat(response, avatar_style="bottts", key=str(i))  # Model response