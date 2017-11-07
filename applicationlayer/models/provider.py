from ..globals.mongodatabase import MongoDatabase


class ProviderEntity:

    def __init__(self):
        pass

    @property
    def mongo_connector(self):
        return MongoDatabase(self)


class ProviderBalance:

    def __init__(self):
        pass

    @property
    def mongo_connector(self):
        return MongoDatabase(self)
