# -*- coding: utf-8 -*-
"""
Created on Thu May 22 09:27:58 2025

@author: Chih-Yi
"""
import pandas as pd
import configparser
import mysql.connector
from mysql.connector import Error

if __name__ == "__main__":
    file = 'data1.csv'
    data = pd.read_csv(open(file))
    
    ## 讀取設定檔
    config = configparser.ConfigParser()
    config.read('./control/Setting.ini')
    
    host = config['Set']['host']
    username = config['Set']['user']
    password = config['Set']['password']
    database = config['Set']['database']
    table_name = config['Set']['datatabel']
    
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
    
