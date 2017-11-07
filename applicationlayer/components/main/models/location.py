from applicationlayer.globals.mongodatabase import MongoDatabase


class Locations:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)