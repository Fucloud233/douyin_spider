# -*- coding = utf-8 -*-
# @Time : 2023/07/13 15:13
# @Autor : Fucloud
# @FIle : fmt.py
# @Software : PyCharm


def debug(text: str):
    text_list = text.split('\n')
    for text in text_list:
        print("[debug] " + text)


def info(text: str):
    text_list = text.split('\n')
    for text in text_list:
        print("[info] " + text)
