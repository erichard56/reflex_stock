# from sqlmodel import create_engine
import sqlite3

DATABASE = './stock.db'

def connect():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor
    # engine = create_engine('sqlite:///' + DATABASE, echo=False)
    # return engine


