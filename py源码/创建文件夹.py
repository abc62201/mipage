import os
from 写入index import *
from 写入css import *
from 写入js import *
def 创建文件夹(path):
    当前路径 = os.getcwd()
    folder_path= os.path.join(当前路径, path)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
def 写入内容(file_path,file_words):
    if os.path.exists(file_path): return
    with open(file_path, "w",encoding='utf-8') as file:
            file.write(file_words)

def 创建默认路径():
    创建文件夹("html")
    创建文件夹("html/images")
    写入内容("html/index.css",主页默认样式())
    写入内容("html/index.js",主页默认脚本())
    写入内容("html/index.html",主页默认文本())
    