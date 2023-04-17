import time

import gradio as gra


def user_greeting(name):
    time.sleep(10)
    return "Hi! " + name + " Welcome to your first Gradio application!😎"


# define gradio interface and other parameters
app = gra.Interface(
    fn=user_greeting,
    inputs="text",
    outputs="text",
)
app.launch(
    server_name='0.0.0.0', server_port=8888, share=False,show_error=True, enable_queue=True
)
