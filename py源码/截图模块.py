#! python3.15.0
import os
import sqlite3
import threading
import hashlib
from playwright.sync_api import sync_playwright


def 获取网页截图(url, save_path, timeout=30000):
    """
    使用系统浏览器截取网页快照
    """
    try:
        with sync_playwright() as p:
            # 优先使用系统已安装的浏览器
            browser_paths = [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            
            browser = None
            for path in browser_paths:
                if os.path.exists(path):
                    try:
                        browser = p.chromium.launch(headless=True, executable_path=path)
                        print(f"✅ 使用系统浏览器: {path}")
                        break
                    except Exception as e:
                        print(f"⚠️ 无法使用 {path}: {e}")
                        continue
            
            if not browser:
                print("❌ 未找到系统浏览器，截图失败")
                return False
            
            page = browser.new_page(viewport={'width': 1280, 'height': 720})
            page.goto(url, timeout=timeout, wait_until='networkidle')
            page.wait_for_timeout(2000)
            page.screenshot(path=save_path, full_page=False)
            browser.close()
            return True
    except Exception as e:
        print(f"截图失败 [{url}]: {e}")
        return False


# 其他函数保持不变...


def 生成截图文件名(url):
    """根据URL生成唯一的文件名"""
    hash_obj = hashlib.md5(url.encode('utf-8'))
    return f"{hash_obj.hexdigest()}.png"


def 获取图片目录():
    """获取图片存储目录的绝对路径"""
    return os.path.join(os.getcwd(), "html", "images")


def 检查是否需要截图(url, image):
    """
    检查是否需要截图
    :param url: 网页URL
    :param image: 数据库中存储的图片路径
    :return: 是否需要截图
    """
    if not url:
        return False
    
    if not image:
        return True
    
    # 检查文件是否存在
    if image.startswith('images/'):
        check_path = os.path.join(os.getcwd(), "html", image)
    elif os.path.isabs(image):
        check_path = image
    else:
        check_path = os.path.join(获取图片目录(), image)
    
    return not os.path.exists(check_path)


def 异步截图单条记录(record_id, url):
    """异步截图单条记录"""
    try:
        images_dir = 获取图片目录()
        
        # 确保图片目录存在
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        
        # 生成文件名
        filename = 生成截图文件名(url)
        save_path = os.path.join(images_dir, filename)
        
        print(f"📸 [{record_id}] 正在截图: {url[:50]}...")
        
        # 截取网页快照
        if 获取网页截图(url, save_path):
            # 更新数据库
            relative_path = f"images/{filename}"
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            cursor.execute("UPDATE pws_vault SET image=? WHERE id=?", (relative_path, record_id))
            conn.commit()
            conn.close()
            print(f"✅ [{record_id}] 截图成功: {filename}")
        else:
            print(f"❌ [{record_id}] 截图失败")
    except Exception as e:
        print(f"❌ [{record_id}] 截图出错: {e}")


def 启动单条截图线程(record_id, url):
    """启动单条记录的截图线程"""
    thread = threading.Thread(
        target=异步截图单条记录,
        args=(record_id, url),
        daemon=True
    )
    thread.start()
    return thread


def 后台截图任务():
    """后台线程：自动获取所有记录的网页截图"""
    db_file = "webps.data"
    images_dir = 获取图片目录()
    
    # 确保图片目录存在
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 查询所有有URL的记录
        cursor.execute("""
            SELECT id, url, image FROM pws_vault 
            WHERE url IS NOT NULL AND url != ''
        """)
        records = cursor.fetchall()
        
        if not records:
            print("✅ 数据库中没有任何需要截图的记录。")
            conn.close()
            return
        
        # 筛选需要截图的记录
        need_screenshot = []
        for record_id, url, image in records:
            expected_filename = 生成截图文件名(url)
            expected_path = os.path.join(images_dir, expected_filename)
            
            # 情况1: 数据库image字段为空
            if not image or image == '':
                need_screenshot.append((record_id, url, expected_filename))
                continue
            
            # 情况2: 数据库有记录，但文件不存在
            if image.startswith('images/'):
                check_path = os.path.join(os.getcwd(), "html", image)
            elif os.path.isabs(image):
                check_path = image
            else:
                check_path = os.path.join(images_dir, image)
            
            if not os.path.exists(check_path):
                need_screenshot.append((record_id, url, expected_filename))
                continue
            
            # 情况3: 文件存在但文件名不匹配，更新数据库
            if image != f"images/{expected_filename}":
                cursor.execute("UPDATE pws_vault SET image=? WHERE id=?", 
                             (f"images/{expected_filename}", record_id))
                conn.commit()
        
        conn.commit()
        
        if not need_screenshot:
            print("✅ 所有截图文件都存在，无需更新。")
            conn.close()
            return
        
        print(f"📸 发现 {len(need_screenshot)} 条记录需要截图...")
        
        success_count = 0
        for record_id, url, filename in need_screenshot:
            save_path = os.path.join(images_dir, filename)
            
            print(f"  🔄 [{record_id}] 正在截图: {url[:60]}...")
            
            if 获取网页截图(url, save_path):
                relative_path = f"images/{filename}"
                cursor.execute("UPDATE pws_vault SET image=? WHERE id=?", (relative_path, record_id))
                conn.commit()
                success_count += 1
                print(f"  ✅ [{record_id}] 截图成功: {filename}")
            else:
                print(f"  ❌ [{record_id}] 截图失败")
        
        conn.close()
        print(f"\n🎉 截图任务完成！成功: {success_count}/{len(need_screenshot)}")
        
    except Exception as e:
        print(f"❌ 截图任务出错: {e}")
        if 'conn' in locals():
            conn.close()


def 启动截图线程():
    """启动后台截图线程"""
    thread = threading.Thread(target=后台截图任务, daemon=True)
    thread.start()
    return thread