from applicationlayer.globals.mongodatabase import MongoDatabase


class Supplier:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)


class SupplierProductRel:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)
