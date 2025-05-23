import os
import sys
import pandas as pd
import configparser
import sqlite3

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))  # 切換到目前這個 Python 檔案的目錄

    file = '../input/data1.csv'
    data = pd.read_csv(open(file, encoding='Big5'))

    config = configparser.ConfigParser()
    config.read('../control/Setting.ini')

    db_path = config['SQLite']['sqlite_path'] # SQLite 資料庫路徑
    table_name = config['SQLite']['datatabel'] # 資料表名稱

    try:
        connection = sqlite3.connect(db_path)
        print("Connected to SQLite database")

        cursor = connection.cursor()

        # 建立欄位名稱清單
        columns = data.columns.tolist()

        for _, row in data.iterrows():
            placeholders = ', '.join(['?'] * len(row))
            col_names = ', '.join(columns)
            update_clause = ', '.join([f"{col}=excluded.{col}" for col in columns])

            sql_query = f"""
            INSERT INTO {table_name} ({col_names})
            VALUES ({placeholders})
            ON CONFLICT(date, stock_symbol) DO UPDATE SET
            {update_clause}
            """
            cursor.execute(sql_query, tuple(row))

        connection.commit()
        print(f"Data inserted/updated successfully")

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
