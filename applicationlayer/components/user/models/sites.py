from applicationlayer.globals.mongodatabase import MongoDatabase


class Sites:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)


