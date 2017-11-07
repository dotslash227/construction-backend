from ..globals.mongodatabase import MongoDatabase


class User:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)
