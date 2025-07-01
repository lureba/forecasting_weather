import psycopg2 as pg
import os
dbname = os.getenv("DBNAME")
host = os.getenv("HOST")
user = os.getenv("USER_POSTGRES")
password = os.getenv("PASSWORD")
conn = pg.connect("host={} dbname={} user={} password={}".format(host,dbname,user,password))

curs = conn.cursor()
curs.execute('''CREATE TABLE IF NOT EXISTS WEATHER_(
             city_name VARCHAR(100),
             main VARCHAR(100),
             actual_temp NUMERIC(5,2),
             feels_like NUMERIC(5,2),
             temp_min NUMERIC(5,2),
             temp_max NUMERIC(5,2),
             actual_date timestamp,
             humidity INTEGER,
             pressure INTEGER,
             sunset timestamp,
             sunrise timestamp
             )
             '''
             )

conn.commit()
curs.close()
conn.close()