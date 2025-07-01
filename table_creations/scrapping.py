import psycopg2 as pg
import os

dbname = os.getenv("DBNAME")
user = os.getenv("USER_POSTGRES")
password = os.getenv("PASSWORD")
conn = pg.connect("user={} password={} dbname={}",user,password,dbname)

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS scrapping(
                    category VARCHAR(100),
                    text VARCHAR(1000),
                    date_scrap DATE,
                    url VARCHAR(300)
               )''')

conn.commit()
cursor.close()
conn.close()