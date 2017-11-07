from ..utils.config import MongoCredentials as MongoCred
from .initiate_db_connections import initiate_mongo_connection


class MongoConnections(object):

  def __init__(self, db=MongoCred().db):
    self._mongo_db = client[str(db)]

  @property
  def mongo_db(self):
    return self._mongo_db


client = initiate_mongo_connection()
