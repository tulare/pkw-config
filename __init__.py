# -*- encoding: utf-8 -*-

import os
import sqlite3

CONF_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.dirname(CONF_PATH)

class Configuration :

    def __init__(self) :
        self.database = CONF_PATH + '/database.db'

        # creation table config si nécessaire
        with sqlite3.connect(self.database) as db :
            db.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key STRING PRIMARY KEY,
                    value STRING NOT NULL
                )
            """)

    def get(self, key, default=None) :
        with sqlite3.connect(self.database) as db :
            cursor = db.execute(
                "SELECT value FROM config WHERE key = ?",
                (key,)
            )
            row = cursor.fetchone()
            try :
                return row[0]
            except :
                return default
        
    def set(self, key, value) :
        with sqlite3.connect(self.database) as db :
            try :
                # insert
                cursor = db.execute(
                    "INSERT INTO config VALUES(? , ?)",
                    (key, value)
                )
            except sqlite3.IntegrityError as e :
                # update
                cursor = db.execute(
                    "UPDATE config SET value = ? WHERE key = ?",
                    (value, key)
                )
            finally :
                # commit
                db.commit()

            return cursor.rowcount
        
    def delete(self, key) :
        with sqlite3.connect(self.database) as db :
            try :
                # delete
                cursor = db.execute(
                    "DELETE FROM config WHERE key = ?",
                    (key,)
                )
            finally :
                # commit
                db.commit()

            return cursor.rowcount

    @property        
    def items(self) :
        with sqlite3.connect(self.database) as db :
            # select
            cursor = db.execute("SELECT * FROM config")
            return dict(cursor.fetchall())
        
