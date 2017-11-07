from applicationlayer.globals.mongodatabase import MongoDatabase


class InventoryMaster:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)
