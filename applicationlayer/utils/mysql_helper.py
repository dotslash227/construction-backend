from ..globals.mysql_connections import MYSQLConnections
from .exception_utils import LogExceptions

# TODO: Update code for C, U, D (R is done)
class MYSQLQueryUtils:

  def __init__(self):
    self.db_conn = MYSQLConnections().mysql_db

  def get_data(self, query):
    queried_data = []
    try:
      print query
      data = self.db_conn.execute(query)
      queried_data = data.fetchall()
    except Exception as e:
      LogExceptions().log_exception(e.message)
    return queried_data

  def update(self, query):
    try:
      self.db_conn.execute(query)
    except Exception as e:
      LogExceptions().log_exception(e.message)

  def insert(self, query):
    try:
      cursor =  self.db_conn.execute(query)
      if cursor:
        return cursor.lastrowid
    except Exception as e:
      LogExceptions().log_exception(e.message)

  def delete(self, query):
    try:
      self.db_conn.execute(query)
    except Exception as e:
      LogExceptions().log_exception(e.message)
