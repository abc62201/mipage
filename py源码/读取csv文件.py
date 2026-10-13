#! python3.15.0
import csv
import sqlite3
import os
import glob

def 验证CSV表头(csv_file):
    """
    验证CSV文件表头是否包含必需字段
    必需字段: name, url, username, password, note
    可选字段: classify
    """
    required_fields = {'name', 'url', 'username', 'password', 'note'}
    
    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # 读取第一行表头
            
            if header is None:
                return False, "文件为空"
            
            # 将表头转为小写并去除空格，增加容错性
            header_set = set(h.strip().lower() for h in header)
            
            # 检查是否包含所有必需字段
            missing_fields = required_fields - header_set
            if missing_fields:
                return False, f"缺少必需字段: {', '.join(missing_fields)}"
            
            # 检查是否有 classify 字段（可选）
            has_classify = 'classify' in header_set
            
            return True, header, has_classify
            
    except Exception as e:
        return False, f"读取失败: {e}", False


def 扫描并导入所有CSV(db_file="webps.data"):
    """
    扫描当前目录下所有CSV文件，验证表头后智能导入，导入完成后删除文件
    """
    # 获取当前目录下所有CSV文件
    csv_files = glob.glob("*.csv")
    
    if not csv_files:
        print("💡 当前目录下未找到任何CSV文件。")
        return
    
    print(f"🔍 发现 {len(csv_files)} 个CSV文件，开始检查...")
    
    total_imported = 0
    
    for csv_file in csv_files:
        print(f"\n📄 正在处理: {csv_file}")
        
        # 验证表头
        result = 验证CSV表头(csv_file)
        is_valid = result[0]
        
        if not is_valid:
            print(f"   ⚠️ 表头不匹配，跳过导入。原因: {result[1]}")
            continue
        
        header = result[1]
        has_classify = result[2] if len(result) > 2 else False
        
        if has_classify:
            print(f"   ✅ 表头验证通过（含classify字段）: {header}")
        else:
            print(f"   ✅ 表头验证通过（无classify字段，将使用默认分类）: {header}")
        
        # 执行智能导入
        imported_count = 智能导入CSV(csv_file, db_file, has_classify)
        total_imported += imported_count
        
        # 导入完成后删除CSV文件（无论是否导入新数据）
        删除CSV文件(csv_file)
    
    print(f"\n{'='*50}")
    print(f"🎉 全部处理完成！共导入 {total_imported} 条新记录。")


def 智能导入CSV(csv_file, db_file="webps.data", has_classify=False):
    """
    智能导入单个CSV文件：只导入数据库中不存在的新数据
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 步骤1: 从数据库查询已有的 (url, username) 组合
        cursor.execute("SELECT url, username FROM pws_vault")
        existing_records = set(cursor.fetchall())
        
        # 步骤2: 读取CSV文件并筛选出新数据
        new_data = []
        with open(csv_file, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # 将字段名统一为小写，增加容错性
            for row in reader:
                # 统一键名为小写
                row_lower = {k.strip().lower(): v for k, v in row.items()}
                
                name = row_lower.get('name', '')
                url = row_lower.get('url', '')
                username = row_lower.get('username', '')
                password = row_lower.get('password', '')
                note = row_lower.get('note', '')
                
                # 读取 classify 字段，如果没有则默认为"未分类"
                if has_classify:
                    classify = row_lower.get('classify', '未分类')
                    if not classify or classify.strip() == '':
                        classify = '未分类'
                else:
                    classify = '未分类'
                
                # 检查这条记录是否已存在于数据库
                if (url, username) not in existing_records:
                    new_data.append((classify, name, url, username, password, note))
                    # 加入已有记录集合，避免CSV内部重复
                    existing_records.add((url, username))
        
        # 步骤3: 只插入新数据
        if new_data:
            sql_insert = """
            INSERT INTO pws_vault (classify, name, url, username, password, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.executemany(sql_insert, new_data)
            conn.commit()
            print(f"   ✅ 成功导入 {len(new_data)} 条新记录！")
        else:
            print(f"   ✅ 没有新数据需要导入。")
        
        return len(new_data)
        
    except Exception as e:
        print(f"   ❌ 导入失败: {e}")
        return 0
    finally:
        if 'conn' in locals():
            conn.close()


def 删除CSV文件(csv_file):
    """
    删除已处理的CSV文件
    """
    try:
        if os.path.exists(csv_file):
            os.remove(csv_file)
            print(f"   🗑️ 已删除文件: {csv_file}")
    except PermissionError:
        print(f"   ⚠️ 无法删除文件（被占用）: {csv_file}")
    except Exception as e:
        print(f"   ⚠️ 删除文件失败: {csv_file} - {e}")


if __name__ == "__main__":
    扫描并导入所有CSV()