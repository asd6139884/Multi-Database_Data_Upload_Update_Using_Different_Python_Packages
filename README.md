# MySQL Data Upload/Update Using Different Python Packages

本專案使用不同的 Python 套件（`mysql.connector`、`PyMySQL`、`mysqlclient`、`SQLAlchemy`）連接 MySQL 資料庫，實現將 CSV 資料上傳或更新到資料庫的功能。

## 套件比較
- `mysql-connector-python`：
  - 是官方提供的純 Python 實現，穩定可靠。
  - 安裝：`pip install mysql-connector-python`
- `PyMySQL`：
  - 完全用 Python 實作，安裝方便，常用於輕量或快速開發。
  - 安裝：`pip install pymysql`
- `MySQLdb (mysqlclient)`：
  - C 語言底層驅動，效能較好，但安裝上較麻煩，需要先裝好 MySQL 的開發套件。
  - `mysqlclient` 是 MySQLdb 的 fork，需要事先安裝好 MySQL 開發環境。使用上跟 `PyMySQL` 類似，但模組名稱不同。
  - 安裝：`pip install mysqlclient`
- `SQLAlchemy`：
  - 不是直接連接 MySQL 的驅動，而是 ORM 框架，可以透過它搭配上述驅動來操作資料庫。它讓你用物件導向方式操作資料庫，更適合複雜專案。
  - 安裝：`pip install sqlalchemy`

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





