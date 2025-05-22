from sqlalchemy import create_engine
import configparser
import pandas as pd
from sqlalchemy import text


config = configparser.ConfigParser()
config.read('./control/Setting.ini')

host = config['Set']['host']
username = config['Set']['user']
password = config['Set']['password']
database = config['Set']['database']
table_name = config['Set']['datatabel']

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8mb4")
with engine.begin() as conn:
    current_db = conn.execute(text("SELECT DATABASE();")).scalar()
    print("目前資料庫：", current_db)

    test_query = conn.execute(text("SELECT * FROM stock.daily LIMIT 5"))
    for row in test_query:
        print(row)




