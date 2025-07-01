import psycopg2 as pg
import requests
import os

dbname = os.getenv("DBNAME")
host = os.getenv("HOST")
user = os.getenv("USER_POSTGRES")
password = os.getenv("PASSWORD")
conn = pg.connect("host={} dbname={} user={} password={}".format(host,dbname,user,password))
curs = conn.cursor()

curs.execute('''CREATE TABLE IF NOT EXISTS coordinates( 
             city_name VARCHAR(100),
             longitude NUMERIC(8,5),
             latitude NUMERIC(8,5)
             )
             ''')

conn.commit()