import os
import shutil

import gradio as gr

from clc.langchain_application import LangChainApplication

os.environ["CUDA_VISIBLE_DEVICES"] = '0'


# 修改成自己的配置！！！
class LangChainCFG:
    llm_model_name = 'THUDM/chatglm-6b-int4-qe'  # 本地模型文件 or huggingface远程仓库
    embedding_model_name = 'GanymedeNil/text2vec-large-chinese'  # 检索模型文件 or huggingface远程仓库
    vector_store_path = './cache'
    docs_path = './docs'


config = LangChainCFG()
application = LangChainApplication(config)


def get_file_list():
    if not os.path.exists("docs"):
        return []
    return [f for f in os.listdir("docs")]


file_list = get_file_list()


def upload_file(file):
    if not os.path.exists("docs"):
        os.mkdir("docs")
    filename = os.path.basename(file.name)
    shutil.move(file.name, "docs/" + filename)
    # file_list首位插入新上传的文件
    file_list.insert(0, filename)
    application.source_service.add_document("docs/" + filename)
    return gr.Dropdown.update(choices=file_list, value=filename)


def clear_session():
    return '', None


def predict(input,
            large_language_model,
            embedding_model,
            history=None):
    # print(large_language_model, embedding_model)
    print(input)
    if history == None:
        history = []
    resp = application.get_knowledge_based_answer(
        query=input,
        history_len=1,
        temperature=0.1,
        top_p=0.9,
        chat_history=history
    )
    history.append((input, resp['result']))
    search_text = ''
    for idx, source in enumerate(resp['source_documents'][:2]):
        sep = f'----------【搜索结果{idx}：】---------------\n'
        search_text += f'{sep}\n{source.page_content}\n\n'
    print(search_text)
    return '', history, history, search_text


block = gr.Blocks()
with block as demo:
    gr.Markdown("""<h1><center>Chinese-LangChain</center></h1>
        <center><font size=3>
        </center></font>
        """)
    state = gr.State()

    with gr.Row():
        with gr.Column(scale=1):
            embedding_model = gr.Dropdown([
                "text2vec-base"
            ],
                label="Embedding model",
                value="text2vec-base")

            large_language_model = gr.Dropdown(
                [
                    "ChatGLM-6B-int4",
                ],
                label="large language model",
                value="ChatGLM-6B-int4")

            with gr.Tab("select"):
                selectFile = gr.Dropdown(file_list,
                                         label="content file",
                                         interactive=True,
                                         value=file_list[0] if len(file_list) > 0 else None)
            with gr.Tab("upload"):
                file = gr.File(label="请上传知识库文件",
                               file_types=['.txt', '.md', '.docx', '.pdf']
                               )

            file.upload(upload_file,
                        inputs=file,
                        outputs=selectFile)
        with gr.Column(scale=4):
            with gr.Row():
                with gr.Column(scale=4):
                    chatbot = gr.Chatbot(label='Chinese-LangChain').style(height=400)
                    message = gr.Textbox(label='请输入问题')
                    with gr.Row():
                        clear_history = gr.Button("🧹 清除历史对话")
                        send = gr.Button("🚀 发送")
                with gr.Column(scale=2):
                    search = gr.Textbox(label='搜索结果')

        # 发送按钮 提交
        send.click(predict,
                   inputs=[
                       message, large_language_model,
                       embedding_model, state
                   ],
                   outputs=[message, chatbot, state, search])

        # 清空历史对话按钮 提交
        clear_history.click(fn=clear_session,
                            inputs=[],
                            outputs=[chatbot, state],
                            queue=False)

        # 输入框 回车
        message.submit(predict,
                       inputs=[
                           message, large_language_model,
                           embedding_model, state
                       ],
                       outputs=[message, chatbot, state, search])

demo.queue(concurrency_count=2).launch(server_name='0.0.0.0', server_port=8888, share=False,show_error=True, enable_queue=True)
