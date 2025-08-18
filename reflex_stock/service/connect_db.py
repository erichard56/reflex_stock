# import mysql.connector
import sqlite3

DATABASE = './stock.db'

def connect():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="Mer2#lin",
#   database="apasiona_mstocks"
# )

# mydb = mysql.connector.connect(
#   host = '45.227.160.222',
#   user = 'mstock',
#   password = 'locolindol2020!!',
#   database = 'mstockdb2025'
# )


# cursor = mydb.cursor()

