from ..models.product import Product as ProductORM
from ..models.supplier import SupplierProductRel
from applicationlayer.utils.helpers import get_next_sequence


class Product:

    def __init__(self):
        self.product_collection = ProductORM().mongo_connector.apply
        self.supplier_prod_rel = SupplierProductRel().mongo_connector.apply

    def create_products(self, data_dict, site_id):
        prod_id = get_next_sequence('prod')
        data_dict['siteId'] = site_id
        data_dict['prodId'] = prod_id
        data_dict['deleted'] = False
        self.product_collection.insert(data_dict)
        return{'recored': True, 'payload': data_dict}

    def get_products(self, _filers, site_id):
        mongo_query = {'deleted': False, 'siteId': site_id}
        if 'prodId' in _filers:
            mongo_query['prodId'] = {'$in': _filers.get('prodId').split(',')}

        products = self.product_collection.find(mongo_query, {'_id': 0})

        return {'data': list(products)}

    def delete_product(self, prod_id):

        self.product_collection.update(
            {'prodId': prod_id}, {'$set': {'deleted': True}}, multi=True)
        self.supplier_prod_rel.update(
            {'prodId': prod_id},
            {
                '$set': {'deleted': True}
            }, multi=True)
        return {'deleted': True}

    def create_mixture(self, data_dict, site):
        data_dict['category'] = 'mixture'
        prod_id = get_next_sequence('prod')
        data_dict['prodId'] = prod_id
        data_dict['siteId'] = site
        data_dict['deleted'] = False
        self.product_collection.insert_one(data_dict)
        return {'status': 'success', 'data': data_dict}

    def edit_mixture(self, data_dict, site):
        self.product_collection.update(
            {'prodId': data_dict['prodId']}, {'$set': data_dict})
        return {'status': 'success'}
