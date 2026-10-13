#! python3.15.0
import sqlite3
import webbrowser
import threading
from 截图模块 import 检查是否需要截图, 启动单条截图线程, 启动截图线程
from 导出csv import 导出所有记录到CSV, 导出分类到CSV


# API 类：暴露给前端 JavaScript 调用
class API:
    def 获取所有分类(self):
        """获取数据库中所有不重复的分类"""
        try:
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT classify FROM pws_vault WHERE classify IS NOT NULL AND classify != '' ORDER BY classify")
            result = cursor.fetchall()
            conn.close()
            return [row[0] for row in result]
        except Exception as e:
            print(f"获取分类失败: {e}")
            return []
    
    def 添加分类(self, classify_name):
        """添加新分类（插入一条带唯一标识的占位记录）"""
        try:
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            # 使用 classify://分类名 作为唯一URL，确保不违反 UNIQUE(url, username) 约束
            cursor.execute("""
                INSERT OR IGNORE INTO pws_vault (classify, name, url, username, password, note)
                VALUES (?, '占位记录', ?, '__classify__', '', '')
            """, (classify_name, f"classify://{classify_name}"))
            conn.commit()
            conn.close()
            return {"success": True, "message": "分类添加成功"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    def 重命名分类(self, old_name, new_name):
        """重命名分类（批量修改该分类下所有记录的classify字段）"""
        try:
            if not new_name or not new_name.strip():
                return {"success": False, "message": "分类名称不能为空"}
            
            new_name = new_name.strip()
            
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            
            # 检查新名称是否已存在
            cursor.execute("SELECT COUNT(*) FROM pws_vault WHERE classify=?", (new_name,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return {"success": False, "message": f"分类 '{new_name}' 已存在"}
            
            # 批量更新分类名
            cursor.execute("UPDATE pws_vault SET classify=? WHERE classify=?", (new_name, old_name))
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            return {"success": True, "message": f"已将分类 '{old_name}' 重命名为 '{new_name}'（共 {affected} 条记录）"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def 删除分类(self, classify_name):
        """删除分类（批量删除该分类下所有记录）"""
        try:
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            
            # 先查询该分类下有多少条记录
            cursor.execute("SELECT COUNT(*) FROM pws_vault WHERE classify=?", (classify_name,))
            count = cursor.fetchone()[0]
            
            # 批量删除
            cursor.execute("DELETE FROM pws_vault WHERE classify=?", (classify_name,))
            conn.commit()
            conn.close()
            
            return {"success": True, "message": f"已删除分类 '{classify_name}'（共 {count} 条记录）", "count": count}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def 获取分类下的数据(self, classify, keyword=""):
        """获取指定分类下的所有数据，支持按name搜索"""
        try:
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            
            if keyword:
                cursor.execute("""
                    SELECT id, classify, name, url, username, password, note, image 
                    FROM pws_vault 
                    WHERE classify = ? AND name LIKE ?
                    ORDER BY name
                """, (classify, f"%{keyword}%"))
            else:
                cursor.execute("""
                    SELECT id, classify, name, url, username, password, note, image 
                    FROM pws_vault 
                    WHERE classify = ?
                    ORDER BY name
                """, (classify,))
            
            result = cursor.fetchall()
            conn.close()
            
            data_list = []
            for row in result:
                data_list.append({
                    "id": row[0],
                    "classify": row[1],
                    "name": row[2],
                    "url": row[3],
                    "username": row[4],
                    "password": row[5],
                    "note": row[6],
                    "image": row[7]
                })
            return data_list
        except Exception as e:
            print(f"获取数据失败: {e}")
            return []
    
    def 添加密码记录(self, classify, name, url, username, password, note, image=""):
        """添加新的密码记录"""
        try:
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pws_vault (classify, name, url, username, password, note, image)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (classify, name, url, username, password, note, image))
            
            record_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            if 检查是否需要截图(url, image):
                启动单条截图线程(record_id, url)
            
            return {"success": True, "message": "添加成功"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def 修改密码记录(self, id, classify, name, url, username, password, note, image=""):
        """修改密码记录"""
        try:
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pws_vault 
                SET classify=?, name=?, url=?, username=?, password=?, note=?, image=?
                WHERE id=?
            """, (classify, name, url, username, password, note, image, id))
            conn.commit()
            conn.close()
            
            if 检查是否需要截图(url, image):
                启动单条截图线程(id, url)
            
            return {"success": True, "message": "修改成功"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def 删除密码记录(self, id):
        """删除密码记录"""
        try:
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pws_vault WHERE id=?", (id,))
            conn.commit()
            conn.close()
            return {"success": True, "message": "删除成功"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def 移动到其他分类(self, id, new_classify):
        """移动记录到其他分类"""
        try:
            conn = sqlite3.connect("webps.data")
            cursor = conn.cursor()
            cursor.execute("UPDATE pws_vault SET classify=? WHERE id=?", (new_classify, id))
            conn.commit()
            conn.close()
            return {"success": True, "message": "移动成功"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def 打开浏览器(self, url):
        """用默认浏览器打开URL"""
        if url:
            webbrowser.open(url)
            return True
        return False
    
    def 触发截图任务(self):
        """手动触发后台截图任务"""
        try:
            启动截图线程()
            return {"success": True, "message": "截图任务已启动，请稍后刷新页面查看"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def 导出所有密码(self):
        """导出所有密码记录到CSV文件"""
        return 导出所有记录到CSV()
    
    def 导出当前分类(self, classify):
        """导出当前分类的密码记录到CSV文件"""
        return 导出分类到CSV(classify)