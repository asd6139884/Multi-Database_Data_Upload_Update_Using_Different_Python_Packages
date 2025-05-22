import os
import sys
import pandas as pd
import configparser
import mysql.connector
from mysql.connector import Error


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0]))) #切換到目前這個 Python 檔案的目錄

    file = '../input/data1.csv'
    data = pd.read_csv(open(file))
    
    ## 讀取設定檔
    config = configparser.ConfigParser()
    config.read('../control/Setting.ini')
    
    host = config['MySQL']['host']
    username = config['MySQL']['user']
    password = config['MySQL']['password']
    database = config['MySQL']['database']
    table_name = config['MySQL']['datatabel']
    
    ## 連接資料庫並上傳資料
    try:
        connection = mysql.connector.connect(host=host,
                                             user=username,
                                             password=password,
                                             database=database)
        if connection.is_connected():
            print("Connected to MySQL database")
        cursor = connection.cursor()
        
        for _, row in data.iterrows():
            # 構建 SQL 語句
            sql_query = f"""
            INSERT INTO {table_name} ({', '.join(row.keys())})
            VALUES ({', '.join(['%s'] * len(row))})
            ON DUPLICATE KEY UPDATE
            {', '.join([f'{key}=VALUES({key})' for key in row.keys()])}
            """
            cursor.execute(sql_query, tuple(row))
            
        connection.commit() # 提交變更
        print(f"Data inserted/updated successfully: {cursor.rowcount} row(s) affected")

    except Error as e:
        print(f"Error: {e}")
        connection.rollback()
    
