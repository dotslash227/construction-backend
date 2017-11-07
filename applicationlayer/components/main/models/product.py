from applicationlayer.globals.mongodatabase import MongoDatabase


class Product:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)
