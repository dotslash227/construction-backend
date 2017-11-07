from applicationlayer.globals.mongodatabase import MongoDatabase


class UserSitesRel:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)