import time

from ..models.inventory import InventoryMaster as InventoryMasterORM
from ..models.location import Locations as LocationORM
from ..models.product import Product as ProductORM
from ..models.supplier import Supplier as SupplierORM
from equipment_handler import Equipment
from product_handler import Product


class InventoryMaster:

    def __init__(self):
        self.inventory_collection = InventoryMasterORM().mongo_connector.apply

        self.equipment_obj = Equipment()
        self.product_obj = Product()

    def get_gate_pass_quantity(self, data_dict):

        vehicle = self.equipment_obj.get(
            {'id': data_dict['byEquipmentId']})['data'][0]
        product = self.product_obj.get_products(
            {'prodId': data_dict['materialId']})['data'][0]
        vehicle_capacity = vehicle['capacity']
        product_density = product['density']
        quantity = vehicle_capacity * product_density
        return {'quantity': quantity}

    def record_gate_pass(self, data_dict, user, site_id):

        vehicle = self.equipment_obj.get(
            {'id': data_dict['byEquipmentId']},site_id)['data'][0]
        product = self.product_obj.get_products(
            {'prodId': data_dict['materialId']}, site_id)['data'][0]
        quantity = float(data_dict['quantity'])

        vehicleNo = vehicle['registrationNumber']


        supervisorId = user
        date = time.strftime('%Y-%m-%d')
        _time = time.strftime('%H:%M')
        productId = data_dict['materialId']
        fromlocation = data_dict['fromLocationId']
        tolocation = data_dict['toLocationId']
        equipmentId = data_dict['byEquipmentId']

        final_data = {
            "vehicleNo": vehicleNo,
            "supervisorId": supervisorId,
            "date": date,
            "time": _time,
            "quantity": quantity,
            "productId": productId,
            "fromlocation": fromlocation,
            "tolocation": tolocation,
            "equipmentId": equipmentId,  # which is carrying the material
            "siteId":site_id,
            # optional things
            "to": data_dict.get('to'),  # subcontractor or equipment
            "toEquipmentId": data_dict.get('toEquipmentId'),
            "subContractorId": data_dict.get('subContractorId')

        }

        self.inventory_collection.insert(final_data)

    def get_weights(self, ticket):
        if not ticket['grossWeight']:
            grossWeight = 0
        else:
            grossWeight = float(ticket['grossWeight'])

        if not ticket['tareWeight']:
            tareWeight = 0
        else:
            tareWeight = float(ticket['tareWeight'])

        if not ticket['deduction']:
            deduction = 0
        else:
            deduction = float(ticket['deduction'])

        return grossWeight, tareWeight, deduction

    def record_ticket(self, _ticket, user):

        date = time.strftime('%Y-%m-%d')
        _time = time.strftime('%H:%M')
        grossWeight, tareWeight, deduction = self.get_weights(_ticket)

        quantity = grossWeight - tareWeight - deduction

        final_data = {
            "vehicleNo": _ticket['vehicleNumber'],
            "supervisorId": user,
            "date": date,
            "time": _time,
            "quantity": quantity,
            "productId": _ticket['prodId'],
            "tolocation": _ticket['dropLocation'],
            "supplierId": _ticket['supplierId']
        }

        self.inventory_collection.insert(final_data)

    def get_inventroy(self, location, date):
        prods = self.inventory_collection.distinct(
            'productId', {'tolocation': location, 'date': {'$lte': date}})

        result = []

        for prod in prods:
            _in = self.total_to_location(location, prod, date)
            _out = self.total_from_location(location, prod, date)
            _in_data = self.inventory_collection.find(
                {'tolocation': location, 'productId': prod, 'date': {'$lte': date}})
            _out_data = self.inventory_collection.find(
                {'fromlocation': location, 'productId': prod, 'date': {'$lte': date}})

            final = {
                'present': _in - _out,
                'productId': prod,
                'in': {
                    'total': _in,
                    'data': list(_in_data)
                },
                'out': {
                    'total': _out,
                    'data': list(_out_data)
                }

            }
            result.append(final)

        return {'data': result}

    def total_from_location(self, location, prod, date):
        total = self.inventory_collection.aggregate(
            [
                {'$match': {'fromlocation': location,
                            'productId': prod, 'date': {'$lte': date}}},
                {'$group': {'_id': '$fromlocation', 'total': {'$sum': "$quantity"}}}
            ]
        )

        l = list(total)
        if l:
            total = l[0]['total']
        else:
            total = 0

        return total

    def total_to_location(self, location, prod, date):
        total = self.inventory_collection.aggregate(
            [
                {'$match': {'tolocation': location,
                            'productId': prod, 'date': {'$lte': date}}},
                {'$group': {'_id': '$tolocation', 'total': {'$sum': "$quantity"}}}
            ]
        )
        l = list(total)
        if l:
            total = l[0]['total']
        else:
            total = 0

        return total
