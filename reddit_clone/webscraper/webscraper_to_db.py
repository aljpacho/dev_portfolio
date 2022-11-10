import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

LOCAL_DB_NAME = os.getenv("LOCAL_DB_NAME")
LOCAL_DB_USER = os.getenv("LOCAL_DB_USER")

# TODO: 
# Methods to implement
# connect_to_db 
# get_stories
# insert_stories

class DBConnection:
    def __init__(self, db_name=LOCAL_DB_NAME, db_user=LOCAL_DB_USER):
        self._name = db_name
        self.conn = psycopg2.connect(host="localhost", database=LOCAL_DB_NAME, user=db_user)

    def add_stories(self, stories):
        try:
            cursor = self.conn.cursor()
        except psycopg2.DatabaseError as e:
            return e
        else:
            for story in stories:
                cursor.execute("""
                    INSERT INTO stories (title, author, url, created_at)
                    VALUES ({title}, {author}, {url}, {created_at})
                """.format(**story))
        finally:
            cursor.close()

