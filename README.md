# MySQL Data Upload/Update Using Different Python Packages

本專案使用不同的 Python 套件（`mysql.connector`、`PyMySQL`、`mysqlclient`、`SQLAlchemy`）連接 MySQL 資料庫，實現將 CSV 資料上傳或更新到資料庫的功能。

---

## 專案功能

- 從 CSV 檔讀取資料
- 使用多種 Python MySQL 驅動套件執行資料的新增或更新（`ON DUPLICATE KEY UPDATE`）
- 讀取外部設定檔（`Setting.ini`）以取得資料庫連線資訊

---

## 環境需求

- Python 3.7 以上
- MySQL 資料庫服務
- 安裝以下 Python 套件：
  ```bash
  pip install pandas mysql-connector-python pymysql mysqlclient sqlalchemy
  ```
  
## 使用說明

修改 `./control/Setting.ini` 設定檔，填入你的 MySQL 連線資訊與目標資料表名稱，例如：

   ```ini
   [Set]
   host=localhost
   user=root
   password=yourpassword
   database=testdb
   datatabel=your_table_name
   ```


## 程式架構

- `upload_mysqlconnector.py`：使用官方 `mysql.connector` 實作
- `upload_pymysql.py`：使用 `PyMySQL` 實作
- `upload_mysqlclient.py`：使用 `mysqlclient`（MySQLdb）實作
- `upload_sqlalchemy.py`：使用 `SQLAlchemy` ORM 實作
- `./control/Setting.ini`：資料庫設定檔
- `data.csv`：待上傳資料範例檔案





