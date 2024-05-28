# functions.py

import os
import datetime
import pandas as pd
import gradio as gr
from PIL import Image
from openai import OpenAI
from deep_translator import GoogleTranslator
import prepare as pre
import subprocess

# 一些全局变量
visible = False
image = Image.open(pre.Image_Path)
image_w = Image.open(pre.Image_Path_w)
client = OpenAI(base_url=pre.URL, api_key="not-needed")
time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def current_time():
    def helper():
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return f" {current_time}"

    return helper


def image_processing(input_image):
    try:
        width, height = input_image.size
        new_width = width + width // 2
        new_height = height + height // 2
        new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

        x_offset = (new_width - width) // 2
        y_offset = (new_height - height) // 2
        new_image.paste(input_image, (x_offset, y_offset))
        return new_image
    except Exception as e:
        print("An exception in image processing occurred.")
        gr.Warning('An exception in image processing occurred.')


def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def user(new_input, history_chatbot):
    return "", history_chatbot + [[parse_text(new_input), ""]]


def reset_chat(empty_chatbot):
    pre.prompt = pre.prompt_set[:]
    return empty_chatbot + [[pre.first_chat[0], pre.first_chat[1]]]


def preview_visible():
    global visible
    visible = not visible
    return gr.update(visible=visible)


def predict_response(prompt):
    try:
        # 启动 Llama 服务器
        subprocess.run(
            ["../llama.cpp/server", "--host", "0.0.0.0", "--model", "../model/Meta-Llama-3-8B-Instruct.Q2_K.gguf"])

        # 调用 Llama 模型预测
        response = client.chat_completions.create(
            model="llama",
            messages=prompt,
            temperature=0.7,
        )

        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"An exception occurred: {e}")
        return "An error occurred while generating the response."


def empty_his():
    gr.Info('The History Dialogue has been emptied.')
    return None


def translate(original_input):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(original_input)
        return translated
    except Exception as e:
        print("An exception in translate occurred.")
        gr.Warning('An exception in translate occurred.\nConnecting to a network may solve.')


def save_dialogue(chatbot):
    try:
        dialogues = {'index': [], 'user messages': [], 'model messages': []}
        index = dialogues['index']
        user_msgs = dialogues['user messages']
        model_msgs = dialogues['model messages']
        for idx, (user_msg, model_msg) in enumerate(chatbot):
            index.append(idx)
            user_msgs.append(user_msg)
            model_msgs.append(model_msg)

        pd.DataFrame(dialogues).to_csv(f'{pre.Save_Dialogue_Path}/chatbot_dialogues_{time}.csv')
        gr.Info(f'The dialogue has been saved to directory: {pre.Save_Dialogue_Path}')
    except Exception as e:
        print("An exception in dialogue saving occurred.")
        gr.Warning('An exception in dialogue saving occurred.')


def text_processing(path_lists):
    try:
        text_dict = dict()
        file_list = list()

        for file_path in path_lists:
            if file_path.endswith('.pdf') or file_path.endswith('.docx') or file_path.endswith('.png'):
                file_list += os.path.splitext(file_path)[0]

        for title, text in file_list:
            text_dict[title] = text

        return text_dict
    except Exception as e:
        print("An exception in text processing occurred.")
