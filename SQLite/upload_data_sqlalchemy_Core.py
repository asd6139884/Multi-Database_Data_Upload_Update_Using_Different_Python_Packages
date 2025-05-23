import os
import sys
import pandas as pd
import configparser
from sqlalchemy import create_engine, inspect, Table, Column, Integer, String, MetaData, Float, DateTime
from sqlalchemy.dialects.sqlite import insert


# 根據 Pandas dtype 自動轉換成 SQLAlchemy Column 類型
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
    
    # 建立資料庫檔案（若不存在）
    if not os.path.exists(db_full_path):
        open(db_full_path, 'w').close()
        print(f"🔹 資料庫{db_file}不存在，已自動建立資料庫{db_file}")
        
    # 建立引擎
    engine = create_engine(f'sqlite:///{db_full_path}')   
    connection = engine.connect()

    # 使用 MetaData 映射表
    metadata = MetaData()

    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        # 根據 CSV 自動建立資料表欄位
        columns = []
        for col, dtype in data.dtypes.items():
            col_def = map_dtype_to_column(col, dtype, primary_keys)
            columns.append(col_def)
        # 建立資料表
        my_table = Table(table_name, metadata, *columns)
        metadata.create_all(engine)
        print(f"🔹 資料表{table_name}不存在，已自動建立{table_name}")
    else:
        my_table = Table(table_name, metadata, autoload_with=engine)
        print(f"🔹 資料表{table_name}已存在，使用現有資料表")

    # 將 DataFrame 一列列轉換成 dict 並插入
    for row in data.to_dict(orient='records'):
        stmt = insert(my_table).values(**row)
        update_dict = {col: stmt.excluded[col] for col in row.keys()}
        stmt = stmt.on_conflict_do_update(
            index_elements=primary_keys,
            set_=update_dict
        )
        connection.execute(stmt)
    
    connection.commit()
    connection.close()
    print("✅ 資料寫入完成")
