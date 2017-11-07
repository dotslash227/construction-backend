from .mongo_connections import MongoConnections
from ..utils.config import MongoCredentials


class MongoDatabase:

  def __init__(self, _object, db = MongoCredentials().db):
    mongo_connection = MongoConnections(db= db)
    self.__collection = mongo_connection.mongo_db[_object.__class__.__name__]
    self.apply = self.__collection
