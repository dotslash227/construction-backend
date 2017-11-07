from applicationlayer.globals.mongodatabase import MongoDatabase


class Permissions:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)


class Roles:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)


class UserRolesRel:

    @property
    def mongo_connector(self):
        return MongoDatabase(self)
