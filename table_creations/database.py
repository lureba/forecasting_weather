import psycopg2 as pg
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

dbname = os.getenv("DBNAME")
host = os.getenv("HOST")
user = os.getenv("USER_POSTGRES")
password = os.getenv("PASSWORD")
conn = pg.connect("host={} dbname={} user={} password={}".format(host,dbname,user,password))
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 

crs = conn.cursor()

crs.execute("CREATE DATABASE weather_vale")


conn.commit()
crs.close()
conn.close()