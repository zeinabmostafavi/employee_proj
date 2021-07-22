from datetime import datetime
from os import name
from sqlite3 import connect
from typing import Text
from time import time
import sqlite3


class Database:

    @staticmethod
    def insert(name, familly, national_code, birthday, img):
        try:
            my_con = connect('employee.db')
            my_cursor = my_con.cursor()
            my_cursor.execute(
                f"INSERT INTO user(name,familly,national_code,birthday,img) VALUES('{name}','{familly}', '{national_code}', '{birthday}','{img}')")

            my_con.commit()
            my_con.close()
            return True
        except Exception as e:
            print("error:", e)
            return False

    @staticmethod
    def select():
        try:
            my_con = connect('employee.db')
            my_cursor = my_con.cursor()
            my_cursor.execute("SELECT * FROM user")
            result = my_cursor.fetchall()
            my_con.close()
            return result
        except Exception as e:
            print("error:", e)
            return []

    @staticmethod
    def edit(name, familly, national_code, birthday, img, _id):
        my_con = connect('messages.db')
        my_cursor = my_con.cursor()
        my_cursor.execute(
            f"UPDATE messages SET name='{name}',familly='{familly}',national_code='{national_code}',birthday='{birthday}',img='{img}',edited='{1}' WHERE ID={_id}")
        my_con.commit()
        my_con.close()
        return True
