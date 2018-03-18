from applicationlayer.globals.mongodatabase import MongoDatabase


class Employee:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)
