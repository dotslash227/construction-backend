from ..models.product import Product as ProductORM
from ..models.supplier import Supplier as SupplierORM
from ..models.supplier import SupplierProductRel
from applicationlayer.utils.helpers import get_next_sequence

from bson import ObjectId

from applicationlayer.models.provider import ProviderEntity


class Supplier:

    def __init__(self):
        self.supplier_collection = SupplierORM().mongo_connector.apply
        self.provider_entity_collection = ProviderEntity().mongo_connector.apply
        self.product_collection = ProductORM().mongo_connector.apply
        self.supplier_prod_collection = SupplierProductRel().mongo_connector.apply

    # def change_present_rate(self):

    def update_retrospective_changes(self, data_dict, user):
        # {
        #   "supplierId": "supplier_19",
        #   "entityId": "prod_37",
        #   "rate": [
        #     {
        #       "fromDate": null,
        #       "toDate": null
        #     }
        #   ]
        # }
        user.pop('email')
        supplier_id = data_dict['supplierId']
        prod_id = data_dict['entityId']
        count = 0
        for _cost in data_dict['rate']:
            _gte = _cost['fromDate']
            if _cost.get('tillPresent'):
                _lte = time.time() * 1000
            else:
                _lte = _cost['toDate']

            records = self.provider_entity_collection.find(
                {'createdAt':
                    {
                        '$gte': _gte,
                        '$lte': _lte
                    },
                 'supplierId': supplier_id,
                 'prodId': prod_id
                 },
            )
            for rec in records:
                if rec.get('transportationBy') == 'provider':
                    self.provider_entity_collection.update(
                        {'_id': ObjectId(rec['_id'])},
                        {'$set':
                         {
                             'cost': rec['quantity'] * float(_cost['cost']) + rec['quantity'] * float(_cost['transportCost']),
                             'rate': _cost['cost'],
                             'transportationRate': _cost['transportCost'],
                             'retroEditBy': user,
                             'retroEditAt': time.time() * 1000
                         }
                         }
                    )

                else:
                    self.provider_entity_collection.update(
                        {'_id': ObjectId(rec['_id'])},
                        {'$set':
                         {
                             'cost': rec['quantity'] * float(_cost['cost']),
                             'rate': _cost['cost'],
                             'retroEditBy': user,
                             'retroEditAt': time.time() * 1000

                         }
                         }
                    )
        return {'updated': True}

    def update_supplier(self, data_dict):

        self.supplier_prod_collection.delete_many(
            {'supplierId': data_dict['supplierId']})

        for prod in data_dict.pop('products'):
            prod['supplierId'] = data_dict['supplierId']
            self.supplier_prod_collection.insert(prod)
        self.supplier_collection.update({'supplierId': data_dict['supplierId']},
                                        {'$set': data_dict}
                                        )
        return {'recorded': True, 'payload': data_dict}

    def create_supplier(self, data_dict, site_id):
        data_dict['siteId'] = site_id
        supplier_id = get_next_sequence('supplier')
        data_dict['supplierId'] = supplier_id
        for prod in data_dict.pop('products'):
            prod['supplierId'] = supplier_id
            prod['siteId'] = site_id
            self.supplier_prod_collection.insert(prod)
        self.supplier_collection.insert(data_dict)
        return{'recored': True, 'payload': data_dict}

    def get_suppliers(self, _filers, site_id):
        mongo_query = {'siteId': site_id}
        if 'supplierId' in _filers:
            mongo_query['supplierId'] = {
                '$in': _filers.get('supplierId').split(',')}

        if 'category' in _filers:
            mongo_query['category'] = {
                '$in': _filers.get('category').split(',')}

        suppliers = self.supplier_collection.find(mongo_query, {'_id': 0})
        response = []
        products = {}

        products = {prod['prodId']: prod for prod in self.product_collection.find(
            {'siteId': site_id}, {'_id': 0})}

        for supplier in suppliers:
            supplier['products'] = list(self.supplier_prod_collection.find(
                {'supplierId': supplier['supplierId']}, {'_id': 0}))
            for prod in supplier['products']:
                prod.update(products.get(prod['prodId'], {}))

            response.append(supplier)

        return {'data': response}
