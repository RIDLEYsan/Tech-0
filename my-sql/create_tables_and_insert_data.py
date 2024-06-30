import os
import mysql.connector
from mysql.connector import errorcode

# Obtain the absolute path of the SSL certificate
base_path = os.path.dirname(os.path.abspath(__file__))
ssl_cert_path = os.path.join(base_path, "DigiCertGlobalRootG2.crt.pem")

# Obtain connection string information from the portal
config = {
    "host": "tech0-db-step4-studentrdb-1.mysql.database.azure.com",
    "user": "tech0gen7student",
    "password": "vY7JZNfU",
    "database": "pos_app_arai",
    "client_flags": [mysql.connector.ClientFlag.SSL],
    "ssl_ca": ssl_cert_path,
}

# SQL script to create the tables
sql_script = """
CREATE DATABASE IF NOT EXISTS pos_app_arai;

USE pos_app_arai;

CREATE TABLE IF NOT EXISTS 商品マスタ (
    PRD_ID INT AUTO_INCREMENT PRIMARY KEY,
    CODE CHAR(13) UNIQUE NOT NULL,
    NAME VARCHAR(50) NOT NULL,
    PRICE INT NOT NULL
);

CREATE TABLE IF NOT EXISTS 取引 (
    TRD_ID INT AUTO_INCREMENT PRIMARY KEY,
    DATETIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    EMP_CD CHAR(10),
    STORE_CD CHAR(5),
    POS_NO CHAR(3),
    TOTAL_AMT INT
);

CREATE TABLE IF NOT EXISTS 取引明細 (
    TRD_ID INT,
    DTL_ID INT AUTO_INCREMENT PRIMARY KEY,
    PRD_ID INT,
    PRD_CODE CHAR(13),
    PRD_NAME VARCHAR(50),
    PRD_PRICE INT,
    FOREIGN KEY (TRD_ID) REFERENCES 取引(TRD_ID),
    FOREIGN KEY (PRD_ID) REFERENCES 商品マスタ(PRD_ID)
);
"""

# Construct connection string
try:
    conn = mysql.connector.connect(**config)
    print("Connection established")

    cursor = conn.cursor()
    print("Cursor created")

    # Execute the SQL script to create tables
    for statement in sql_script.split(";"):
        if statement.strip():
            cursor.execute(statement)
            print(f"Executed: {statement.strip()}")

    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print("Error:", err)
else:
    print("Connection closed")
