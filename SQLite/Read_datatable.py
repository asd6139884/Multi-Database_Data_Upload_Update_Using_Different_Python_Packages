import os
import sys
import sqlite3
import configparser
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))  # 切換到目前這個 Python 檔案的目錄

# 資料庫檔案名稱（與 Python 檔案放同一個資料夾）
config = configparser.ConfigParser()
config.read('../control/Setting.ini')

db_filename = config['SQLite']['sqlite_path'] # SQLite 資料庫路徑
table_name = config['SQLite']['datatabel'] # 資料表名稱

# 建立連線
conn = sqlite3.connect(db_filename)

# SQL 查詢語法
sql = f"SELECT * FROM {table_name}"

# 讀取成 DataFrame
df = pd.read_sql_query(sql, conn)

# 顯示資料
print(df)

# 關閉連線
conn.close()
