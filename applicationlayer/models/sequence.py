from ..globals.mongodatabase import MongoDatabase


class Counters:

    def __init__(self):
        pass

    @property
    def mongo_connector(self):
        return MongoDatabase(self)
