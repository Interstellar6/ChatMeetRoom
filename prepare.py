# -*- coding: utf-8 -*-
"""
@File    :   prepare.py
@Time    :   2024/04/30 00:11:46
@Author  :   Krisnile
@Desc    :   This file stored the prepared information.
"""



import multi_agent

"""
-------------------------
    System Preparing
-------------------------
"""
# the connection address
URL = "http://localhost:8080/v1"

# path of files needed
Save_Dialogue_Path = "../data/History_Dialogue"
Image_Path = "../data/Image/kisie-img1.png"
Image_Path_w = "../data/Image/kisie-img2.png"
File_Explorer_Path = "../data/Files/"
File_Extract_Save = "../data/Files/extract_logs/"



"""
-------------------------
    ChatBot Preparing
-------------------------
"""
# some prepared sets of chatbot
prompt_set = [
    {"role": "system",
     "content": "Your name is Kisie, and you are a smart assistant developed by Krismile. You always provide well-thought-out answers that are both correct and useful."},
    {"role": "system", "content": "You are and can only be Kisie, and you always refer to yourself as Kisie."},
    {"role": "system",
     "content": "Your setup is an English AI assistant, so you should respond to all questions in English as much as possible."}
]
prompt = prompt_set[:]

# input hint for the user
hint = "Enter in the inputbox and click 'Submit Input' Button to CHAT!"

# introduction of the application
introduction = "Kisie-v2 is based on the GGUF-quantized Meta open-source model Llama 3-8b, with the following features: \n\
    1. Locally and English Mainly. \n\
    2. The gradio graphical interface can be used. \n\
    3. Diadlog Saving. \n\
    4. Text Translating. \n\
    5. History Clearing. \n\
    Wait to Add: \n\
    6. File Uploading. \n\
    7. Database & SE. \n"

# a dialogue that serves as a cue and a greeting
first_chat = [
    "Say hello to the person who opens the app for the first time and briefly introduce your capability in no more than 30 words.",
    "Hello there! I'm Kisie, your smart companion. I can assist you with tasks, answer questions, provide information, and offer suggestions to make your life easier."
]

"""
-------------------------
    WorkFlow Preparing
-------------------------
"""
# 导入multi_agent中的提示
from multi_agent import prompt0, prompt1, prompt2, prompt3

# 初始化三个不同的任务提示
prompt_set_modeler = [
    {"role": "system", "content": prompt1},
    {"role": "system", "content": "You are and can only be Kisie, and you always refer to yourself as Kisie."},
    {"role": "system",
     "content": "Your setup is an English AI assistant, so you should respond to all questions in English as much as possible."}
]

prompt_set_programmer = [
    {"role": "system", "content": prompt2},
    {"role": "system", "content": "You are and can only be Kisie, and you always refer to yourself as Kisie."},
    {"role": "system",
     "content": "Your setup is an English AI assistant, so you should respond to all questions in English as much as possible."}
]

prompt_set_writer = [
    {"role": "system", "content": prompt3},
    {"role": "system", "content": "You are and can only be Kisie, and you always refer to yourself as Kisie."},
    {"role": "system",
     "content": "Your setup is an English AI assistant, so you should respond to all questions in English as much as possible."}
]

# 为每个任务设置初始提示
prompt_w_modeler = prompt_set_modeler[:]
prompt_w_programmer = prompt_set_programmer[:]
prompt_w_writer = prompt_set_writer[:]

# introduction of the application
introduction_w = "This is Kisie-v2's workflow mode, in which the assistant will answer in the form of a workflow\
    using the appropriate tools below: \n\
        1. search engine. \n\
        ...... \n"
