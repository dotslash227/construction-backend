from ..models.sand import Sand as SandORM
from ..models.sites import Sites as SitesORM
from ..models.trucks import Trucks as TrucksORM

import time


class All:

    def __init__(self):
        self.sites_collection = SitesORM().mongo_connector.apply
        self.trucks_collection = TrucksORM().mongo_connector.apply
        self.sand_collection = SandORM().mongo_connector.apply

    def get_site(self, site_id):
        mongo_query = {}
        if site_id:
            mongo_query['siteId'] = site_id
        site = self.sites_collection.find(
            mongo_query,
            {'_id': 0}
        )
        return {'data': list(site)}

