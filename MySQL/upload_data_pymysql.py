import os
import sys
import pandas as pd
import configparser
import pymysql


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

    try:
        connection = pymysql.connect(host=host,
                                     user=username,
                                     password=password,
                                     database=database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        print("Connected to MySQL database")

        with connection.cursor() as cursor:
            for _, row in data.iterrows():
                sql_query = f"""
                INSERT INTO {table_name} ({', '.join(row.keys())})
                VALUES ({', '.join(['%s'] * len(row))})
                ON DUPLICATE KEY UPDATE
                {', '.join([f'{key}=VALUES({key})' for key in row.keys()])}
                """
                cursor.execute(sql_query, tuple(row))
            connection.commit()
            print(f"Data inserted/updated successfully")

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()

