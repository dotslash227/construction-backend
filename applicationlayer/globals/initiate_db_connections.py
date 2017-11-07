from pymongo import MongoClient
from ..utils.config import MongoCredentials as MongoCred
from ..utils.config import MYSQLCredentials as MYSQLCred
from ..utils.config import URL
from sqlalchemy import create_engine
import redis


def initiate_mongo_connection():
  mongo_client = MongoClient(host=MongoCred().host, port=MongoCred().port, maxPoolSize = 100)
  return mongo_client

def initiate_redis_connection(db=0):
  pool = redis.ConnectionPool(host=URL().redis_ip.split('http://')[1], port=URL().redis_port, max_connections=40, db=db)
  return pool


def initiate_mysql_connection():
  mysql_cred = MYSQLCred()
  mysql_url = mysql_cred.mysql_url
  mysql_pool = create_engine(mysql_url, pool_recycle=mysql_cred.pool_recycle, max_overflow=mysql_cred.max_overflow,
                             pool_size=mysql_cred.pool_size, pool_timeout=mysql_cred.pool_timeout)
  return mysql_pool
