#! python3.15.0
import csv
import sqlite3
import os
from datetime import datetime


def 导出所有记录到CSV(output_file=None):
    """
    将数据库中所有记录导出为CSV文件
    字段顺序: name, url, username, password, note, classify
    兼容Edge浏览器导入，同时保留分类信息
    """
    try:
        # 生成默认文件名
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"密码导出_{timestamp}.csv"
        
        # 连接数据库
        conn = sqlite3.connect("webps.data")
        cursor = conn.cursor()
        
        # 查询所有记录，过滤占位记录和空记录
        cursor.execute("""
            SELECT name, url, username, password, note, classify 
            FROM pws_vault 
            WHERE name IS NOT NULL 
              AND name != '' 
              AND name != '占位记录'
              AND url NOT LIKE 'classify://%'
            ORDER BY classify, name
        """)
        records = cursor.fetchall()
        conn.close()
        
        if not records:
            return {"success": False, "message": "数据库中没有可导出的记录"}
        
        # 写入CSV文件
        with open(output_file, mode='w', encoding='utf-8-sig', newline='') as csvfile:
            # 写入表头（末尾添加classify，兼容浏览器导入）
            writer = csv.writer(csvfile)
            writer.writerow(['name', 'url', 'username', 'password', 'note', 'classify'])
            
            # 写入数据
            for record in records:
                writer.writerow(record)
        
        # 返回完整路径
        full_path = os.path.abspath(output_file)
        return {
            "success": True, 
            "message": f"成功导出 {len(records)} 条记录",
            "count": len(records),
            "file": full_path
        }
        
    except Exception as e:
        return {"success": False, "message": f"导出失败: {e}"}


def 导出分类到CSV(classify, output_file=None):
    """
    导出指定分类的记录到CSV文件
    """
    try:
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_classify = classify.replace('/', '_').replace('\\', '_')
            output_file = f"密码导出_{safe_classify}_{timestamp}.csv"
        
        conn = sqlite3.connect("webps.data")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, url, username, password, note, classify 
            FROM pws_vault 
            WHERE classify = ? 
              AND name IS NOT NULL 
              AND name != '' 
              AND name != '占位记录'
              AND url NOT LIKE 'classify://%'
            ORDER BY name
        """, (classify,))
        records = cursor.fetchall()
        conn.close()
        
        if not records:
            return {"success": False, "message": f"分类 '{classify}' 中没有可导出的记录"}
        
        with open(output_file, mode='w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['name', 'url', 'username', 'password', 'note', 'classify'])
            for record in records:
                writer.writerow(record)
        
        full_path = os.path.abspath(output_file)
        return {
            "success": True,
            "message": f"成功导出分类 '{classify}' 的 {len(records)} 条记录",
            "count": len(records),
            "file": full_path
        }
        
    except Exception as e:
        return {"success": False, "message": f"导出失败: {e}"}