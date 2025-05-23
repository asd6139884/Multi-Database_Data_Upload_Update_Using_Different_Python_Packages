import os
import sys
import pandas as pd
import configparser
from sqlalchemy import create_engine, inspect, Column, Integer, String, Float, DateTime#, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, sessionmaker


# 根據 Pandas dtype 自動轉換成 SQLAlchemy Column 類型
# def map_dtype_to_column(name, dtype):
#     if pd.api.types.is_integer_dtype(dtype):
#         return Column(name, Integer)
#     elif pd.api.types.is_float_dtype(dtype):
#         return Column(name, Float)
#     elif pd.api.types.is_datetime64_any_dtype(dtype):
#         return Column(name, DateTime)
#     else:
#         return Column(name, String)  # 預設為文字
    
def map_dtype_to_column(name, dtype, primary_keys):
    """根據 Pandas dtype 映射到 SQLAlchemy 欄位類型"""
    if pd.api.types.is_integer_dtype(dtype):
        return Column(name, Integer, primary_key=(name in primary_keys))
    elif pd.api.types.is_float_dtype(dtype):
        return Column(name, Float, primary_key=(name in primary_keys))
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return Column(name, DateTime, primary_key=(name in primary_keys))
    else:
        return Column(name, String, primary_key=(name in primary_keys))  # 預設為文字欄位


    
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0]))) #切換到目前這個 Python 檔案的目錄
    
    file = '../input/data1.csv'
    data = pd.read_csv(open(file))

    config = configparser.ConfigParser()
    config.read('../control/Setting.ini')
    db_path = config['SQLite']['db_path'] # SQLite 資料庫路徑
    db_file = config['SQLite']['db_file'] # SQLite 資料庫檔案名稱
    db_full_path = os.path.join(db_path, db_file)
    table_name = config['SQLite']['datatabel'] # 資料表名稱
    primary_keys = [key.strip() for key in config['SQLite']['primary_keys'].split(';')] # 主鍵欄位名稱

    # 設定 ORM 基底
    Base = declarative_base()

    # 動態建立 ORM 類別
    columns = {
        '__tablename__': table_name,
        # '__table_args__': (PrimaryKeyConstraint(*primary_keys),{'extend_existing': True})
        '__table_args__': {'extend_existing': True}
    }
    
    for col, dtype in data.dtypes.items():
        # col_def = map_dtype_to_column(col, dtype)
        col_def = map_dtype_to_column(col, dtype, primary_keys)
        columns[col] = col_def

    MyTable = type(table_name, (Base,), columns)

    # 建立資料庫引擎與 session
    engine = create_engine(f'sqlite:///{db_full_path}')
    Session = sessionmaker(bind=engine)
    session = Session()

    # 檢查資料庫是否存在
    if not os.path.exists(db_full_path):
        Base.metadata.create_all(engine)
        print(f"🔹 資料庫{db_file}不存在，已自動建立資料庫{db_file}和資料表{table_name}")
    else:
        # 檢查資料表是否存在
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            Base.metadata.create_all(engine)
            print(f"🔹 資料表{table_name}不存在，已自動建立{table_name}")
        else:
            print(f"🔹 資料表{table_name}已存在，使用現有資料表")

    # 一筆筆寫入資料(使用 ORM)
    for _, row in data.iterrows():
        record = MyTable(**row.to_dict())
        session.merge(record)  # merge 可以避免重複鍵錯誤
    
    session.commit()
    session.close()
    print("✅ 資料寫入完成")