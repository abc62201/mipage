#! python3.15.0
import sqlite3

def 创建数据库():
# 数据库文件名
    db_file = "webps.data"

# 连接到数据库（如果文件不存在，会自动在当前目录下创建）
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

# 创建表的 SQL 语句
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS pws_vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        classify TEXT,
        name TEXT,
        url TEXT,
        username TEXT,
        password TEXT,
        note TEXT,
        image TEXT,
        UNIQUE(url, username)
    )
    """

# 执行建表 SQL 语句
    cursor.execute(sql_create_table)

# 为 class 和 name 字段分别创建索引，以加快按分类或名称查询的速度
    sql_create_index_class = "CREATE INDEX IF NOT EXISTS idx_classify ON pws_vault(classify);"
    sql_create_index_name = "CREATE INDEX IF NOT EXISTS idx_name ON pws_vault(name);"

    cursor.execute(sql_create_index_class)
    cursor.execute(sql_create_index_name)

# 提交事务并关闭连接
    conn.commit()
    cursor.close()
    conn.close()

#插入数据
def 插入数据(classify, name, url, username, password, note,image,remarks):
    db_file = "webps.data"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    sql_insert = """
    INSERT INTO pws_vault (classify, name, url, username, password, note,image,remarks) VALUES (?, ?, ?, ?, ?, ?,?,?)
    """

    cursor.execute(sql_insert, ())
    conn.commit()