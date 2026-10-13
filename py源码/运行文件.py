#! python3.15.0
import os
import webview
from 建立数据库 import *
from 读取csv文件 import *
from 创建文件夹 import *
from api接口 import API
from 截图模块 import 启动截图线程

创建数据库()
扫描并导入所有CSV()
创建默认路径()

# 启动后台截图线程（不阻塞主程序）
print("🚀 启动后台截图任务...")
启动截图线程()

current_dir = os.getcwd()
index_path = os.path.join(current_dir, "html", "index.html")

# 创建窗口时传入 API 实例
window = webview.create_window(
    title='密码管理器',
    url=index_path,
    maximized=True,
    js_api=API()
)

webview.start()