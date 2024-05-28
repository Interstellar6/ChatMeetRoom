import gradio as gr
from datetime import datetime
import prepare as pre
import functions as func

# 定义全局对话历史记录
history = []

def multi_agent_chat(user_input, chatbot_history):
    global history

    # 用户输入
    history.append(("User", user_input))
    chatbot_history.append(("User", user_input))

    # 各代理生成回复
    modeler_prompt = pre.prompt_set_modeler + [{"role": "user", "content": user_input}]
    programmer_prompt = pre.prompt_set_programmer + [{"role": "user", "content": user_input}]
    writer_prompt = pre.prompt_set_writer + [{"role": "user", "content": user_input}]

    # 各代理生成回复
    modeler_reply = func.predict_response(modeler_prompt)
    history.append(("Modeler", modeler_reply))
    chatbot_history.append(("Modeler", modeler_reply))

    programmer_reply = func.predict_response(programmer_prompt)
    history.append(("Programmer", programmer_reply))
    chatbot_history.append(("Programmer", programmer_reply))

    writer_reply = func.predict_response(writer_prompt)
    history.append(("Writer", writer_reply))
    chatbot_history.append(("Writer", writer_reply))

    return chatbot_history

with gr.Blocks(title="AI Meeting Room") as demo:
    gr.HTML("""<h1 align="start">AI Meeting Room for Math Modeling</h1>""")

    with gr.Tab('ChatBot'):
        with gr.Row():
            with gr.Column():
                gr.Image(type="pil", show_label=False, value=func.image_processing(func.image), container=False,
                         show_download_button=False)
                gr.Textbox(show_label=False, value=pre.introduction, lines=17, interactive=False, container=False)
            with gr.Column(scale=4):
                with gr.Row():
                    with gr.Column(scale=8):
                        chatbot = gr.Chatbot(show_label=False, value=[], container=True, height=520)
                with gr.Row():
                    with gr.Column(scale=6):
                        user_input = gr.Textbox(label="InputBox", placeholder=pre.hint, lines=7, container=False)
                    with gr.Column(scale=3):
                        with gr.Row():
                            emptyBtn = gr.Button("Clear", min_width=10)
                            saveBtn = gr.Button("Save", min_width=10)
                        with gr.Row():
                            submitBtn = gr.Button("Submit Input")

            emptyBtn.click(lambda: [], outputs=[chatbot])
            saveBtn.click(func.save_dialogue, inputs=[chatbot])
            submitBtn.click(multi_agent_chat, inputs=[user_input, chatbot], outputs=[chatbot])

        if __name__ == "__main__":
            demo.queue()
            demo.launch(server_name="0.0.0.0", server_port=8081, inbrowser=True, share=False)

