import os
import sys
import sqlite3
import configparser


os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))  # 切換到目前這個 Python 檔案的目錄

# 資料庫檔案名稱（與 Python 檔案放同一個資料夾）
config = configparser.ConfigParser()
config.read('../control/Setting.ini')

db_filename = config['SQLite']['sqlite_path'] # SQLite 資料庫路徑
table_name = config['SQLite']['datatabel'] # 資料表名稱

# 如果不存在就會自動建立
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# 建立資料表
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    date TEXT,
    stock_symbol TEXT,
    stock_name TEXT,
    transaction_count INTEGER,
    volume INTEGER,
    amount INTEGER,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    price_change REAL,
    PRIMARY KEY (date, stock_symbol)
)
""")

print(f"資料庫與資料表已建立：{db_filename}")

conn.commit()
cursor.close()
conn.close()
