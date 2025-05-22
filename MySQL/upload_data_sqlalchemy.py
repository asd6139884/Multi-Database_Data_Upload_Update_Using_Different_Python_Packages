import os
import sys
import pandas as pd
import configparser
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import text


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0]))) #切換到目前這個 Python 檔案的目錄
    
    file = '../input/data1.csv'
    data = pd.read_csv(open(file))

    config = configparser.ConfigParser()
    config.read('../control/Setting.ini')

    host = config['Set']['host']
    username = config['Set']['user']
    password = config['Set']['password']
    database = config['Set']['database']
    table_name = config['Set']['datatabel']

    # 建立引擎
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8mb4")

    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = Table(table_name, metadata, autoload_with=engine)

    with engine.connect() as conn:
        for _, row in data.iterrows():
            stmt = insert(table).values(**row.to_dict())
            # ON DUPLICATE KEY UPDATE 寫法
            update_dict = {c.name: stmt.inserted[c.name] for c in table.columns}
            stmt = stmt.on_duplicate_key_update(**update_dict)
            conn.execute(stmt)
            conn.commit()  # 需要手動提交
        print("Data inserted/updated successfully")
    
    # with engine.begin() as conn:
    #     for _, row in data.iterrows():
    #         stmt = insert(table).values(**row.to_dict())
    #         # ON DUPLICATE KEY UPDATE 寫法
    #         update_dict = {c.name: stmt.inserted[c.name] for c in table.columns}
    #         stmt = stmt.on_duplicate_key_update(**update_dict)
    #         conn.execute(stmt) # 自動 commit，不需要額外處理
    #     print("Data inserted/updated successfully")