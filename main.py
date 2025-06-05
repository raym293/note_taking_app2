import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
PASS = os.getenv('PASS')
USER = os.getenv('USER')
DATABASE = os.getenv('DATABASE')
DATABASE_URL = os.getenv('DATABASE_URL')
HOST = os.getenv('HOST')
def get_connection():
    try:
        return psycopg2.connect(
            database=DATABASE,
            user="admin",
            password=PASS, 
            host=HOST,
            port=5432,
        )
    except:
        return False
conn = get_connection()
if conn:
    print("Connection to the PostgreSQL established successfully.")
else:
    print("Connection to the PostgreSQL encountered and error.")
    exit()

conn = get_connection()
curr = conn.cursor()
curr.execute("SELECT * FROM notetaker;")
data = curr.fetchall()
async def fn():
    final = ""
    return final
conn.close()