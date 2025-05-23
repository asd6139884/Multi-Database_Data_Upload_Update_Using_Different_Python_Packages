import os
import sys
import sqlite3
import configparser
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))  # 切換到目前這個 Python 檔案的目錄

# 資料庫檔案名稱（與 Python 檔案放同一個資料夾）
config = configparser.ConfigParser()
config.read('../control/Setting.ini')

db_path = config['SQLite']['db_path'] # SQLite 資料庫路徑
db_file = config['SQLite']['db_file'] # SQLite 資料庫檔案名稱
db_full_path = os.path.join(db_path, db_file)
table_name = config['SQLite']['datatabel'] # 資料表名稱

# 建立連線
conn = sqlite3.connect(db_full_path)
cursor = conn.cursor()

# 找出主鍵欄位
cursor.execute(f"PRAGMA table_info({table_name});")
columns_info = cursor.fetchall()
primary_keys = [col[1] for col in columns_info if col[5] > 0]

#查詢資料
sql = f"SELECT * FROM {table_name}" # SQL 查詢語法
df = pd.read_sql_query(sql, conn) # 讀取成 DataFrame

# 顯示資料
print(f'資料庫:{db_full_path},\n資料表:{table_name},\n主鍵欄位：{primary_keys},\n資料:\n{df}')

# 關閉連線
conn.close()
