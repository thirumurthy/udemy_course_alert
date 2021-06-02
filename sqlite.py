# ref https://github.com/myaklov111/awm_atb_bot/blob/master/sqlite.py
import sqlite3
from datetime import datetime
import pytz

__connection = None


def get_connection():
    global __connection
    try:

        if __connection is None:
            __connection = sqlite3.connect("base.db", check_same_thread=False)
        return __connection
    except:
        return None


def unit_db(force: bool = False):
    try:
        conn = get_connection()
        c = conn.cursor()
        if force:
            c.execute('DROP TABLE IF EXISTS udemy')
        c.execute('''
        CREATE TABLE IF NOT EXISTS udemy (
        id             INTEGER PRIMARY KEY,
        site        INTEGER NOT NULL UNIQUE ,
        url      VARCHAR (255) NULL
       )
        ''')
        conn.commit()
        return True
    except Exception as exp:
        print(exp)
        return False


def add_udemy(site: int, url: str):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO udemy (site,url)'
                  ' VALUES (?,?)',
                  (site, url))
        conn.commit()
        return True
    except Exception as exp:
        print(exp)
        return False


def check_url_exists(url: str):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT url FROM udemy WHERE url=?', (url,))
        conn.commit()
        res = c.fetchone()
        if int(res[0]) > -1:
            return True
    except:
        return False
