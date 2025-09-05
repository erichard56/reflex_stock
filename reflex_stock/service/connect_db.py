import mysql.connector
import sqlite3

# DATABASE = './stock.db'

# def connect():
#     conn = sqlite3.connect(DATABASE, check_same_thread=False)
#     cursor = conn.cursor()
#     return conn, cursor

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="Mer2#lin",
#   database="uv029301_mstocks"
# )

# para acceder a la bd de uso en forma remota
mydb = mysql.connector.connect(
  host = '45.227.160.222',
  user = 'uv029301_mstocks',
  password = 'mstocksuv029301mstocks',
  database = 'uv029301_mstocks'
)

# mydb = mysql.connector.connect(
#   host = 'localhost',
#   user = 'uv029301_mstocks',
#   password = 'mstocksuv029301mstocks',
#   database = 'uv029301_mstocks'
# )

cursor = mydb.cursor()

