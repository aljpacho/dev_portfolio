import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

LOCAL_DB_NAME = os.getenv("LOCAL_DB_NAME")
LOCAL_DB_USER = os.getenv("LOCAL_DB_USER")

class DBConnection:
    def __init__(self, db_name=LOCAL_DB_NAME, db_user=LOCAL_DB_USER):
        self._name = db_name
        self.conn = psycopg2.connect(host="localhost", database=db_name, user=db_user)

    def add_stories(self, stories):
        try:
            cursor = self.conn.cursor()
            cursor.executemany(
                """
                INSERT INTO stories (title, url, created_at)
                VALUES (%(title)s, %(url)s, %(created_at)s);
            """,
                stories,
            )

            print("Data inserted into database")
        except psycopg2.DatabaseError as e:
            return e
        else:
            self.conn.commit()
        finally:
            cursor.close()
            self.conn.close()

    def get_stories(self):
        try:
            cursor = self.conn.cursor()
        except psycopg2.DatabaseError as e:
            return e
        else:
            cursor.execute("""SELECT * FROM stories;""")
            print(cursor.fetchall())
        finally:
            cursor.close()
            self.conn.close()
