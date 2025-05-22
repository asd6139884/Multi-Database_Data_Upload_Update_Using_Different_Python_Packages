# Multi-Database Data Upload/Update Using Different Python Packages
本專案旨在使用不同的 Python 套件連接各種 SQL 資料庫，實現 CSV 資料的上傳或更新。
目前已支援 SQLite、MySQL，未來將擴展至其他資料庫，如 PostgreSQL、SQL Server 等。

- 通用
  - `SQLAlchemy`
    - 適用於 MySQL、PostgreSQL、SQLite、SQL Server（需搭配合適的驅動）
    - ORM 框架，可以透過它搭配其他驅動來操作資料庫。它讓你用物件導向方式操作資料庫，更適合複雜專案。
    - 安裝：`pip install sqlalchemy`
- MySQL
  - `mysql.connector`
    - 是官方提供的純 Python 實現，穩定可靠。
    - 安裝：`pip install mysql-connector-python`
  - `PyMySQL`：
    - 完全用 Python 實作，安裝方便，常用於輕量或快速開發。
    - 安裝：`pip install pymysql`
  - `MySQLdb (mysqlclient)`：
    - C 語言底層驅動，效能較好，但安裝上較麻煩，需要先裝好 MySQL 的開發套件。
    - `mysqlclient` 是 MySQLdb 的 fork，需要事先安裝好 MySQL 開發環境。使用上跟 `PyMySQL` 類似，但模組名稱不同。
    - 安裝：`pip install mysqlclient`

## 專案功能
- 從 CSV 讀取資料
- 根據資料庫類型選擇適當的 Python 連接方式
- 讀取外部設定檔（Setting.ini）以取得資料庫連線資訊
- 適用於 MySQL，並規劃擴展至 PostgreSQL、SQLite、SQL Server 等

---

## 環境需求

- Python 3.7 以上
- 已安裝並配置目標 SQL 資料庫
- 必要的 Python 套件（視資料庫類型決定）：
  
## 使用說明

修改 `./control/Setting.ini` 設定檔，填入你的 SQL 連線資訊與目標資料表，例如：

   ```ini
   [Set]
   host=localhost
   user=root
   password=yourpassword
   database=testdb
   datatabel=your_table_name
   ```

## 程式架構
```
├── control/
│   └── Setting.ini  # 資料庫設定檔
├── data.csv  # 待上傳資料
├── MySQL/
│   ├── upload_mysql.py
│   ├── upload_postgresql.py
│   ├── upload_sqlite.py
│   └── upload_sqlserver.py
├── XXX/
```

- `./control/Setting.ini`：資料庫設定檔
- `./input/data.csv`：待上傳資料範例檔案
- MySQL/
  - `upload_mysqlconnector.py`：使用官方 `mysql.connector` 實作
  - `upload_pymysql.py`：使用 `PyMySQL` 實作
  - `upload_mysqlclient.py`：使用 `mysqlclient`（MySQLdb）實作
  - `upload_sqlalchemy.py`：使用 `SQLAlchemy` ORM 實作






