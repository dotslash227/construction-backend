from .initiate_db_connections import initiate_mysql_connection


class MYSQLConnections(object):

  def __init__(self):
    self._mysql_db = client

  @property
  def mysql_db(self):
    return self._mysql_db

  """
  Sample Usage:
  mysql_connections = MYSQLConnections()
	data = mysql_connections.mysql_db.execute('select * from users')
	print data.fetchall()

  """

client = initiate_mysql_connection()
