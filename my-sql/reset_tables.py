import mysql.connector

# データベース接続情報を設定
config = {
    "user": "your_username",
    "password": "your_password",
    "host": "your_server_name.mysql.database.azure.com",
    "database": "your_database_name",
    "raise_on_warnings": True,
}

# データベースに接続
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# 既存のテーブルを削除
cursor.execute("DROP TABLE IF EXISTS 商品マスタ")

# 新しいテーブルを作成
create_table_query = """
CREATE TABLE 商品マスタ (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code CHAR(13) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    price INT NOT NULL
)
"""
cursor.execute(create_table_query)

cnx.commit()
cursor.close()
cnx.close()

print("商品マスタテーブルが再作成されました。")
