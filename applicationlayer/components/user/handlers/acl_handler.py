import numpy as np

from ....models.users import User
from ..models.acl_models import Permissions
from ..models.acl_models import Roles

from ..models.acl_models import UserRolesRel
from ..models.user_sites_rel import UserSitesRel

from applicationlayer.utils.helpers import get_next_sequence


def load_all_roles():
    roles_collection = Roles().mongo_connector.apply
    return {role['id']: role for role in roles_collection.find({}, {'_id': 0})}


def load_all_users():
    user_collection = User().mongo_connector.apply
    return {user['user_id']: user for user in user_collection.find({}, {'_id': 0, 'password': 0})}


all_roles = load_all_roles()
all_users = load_all_users()


class ACL:

    def __init__(self):
        self.roles_collection = Roles().mongo_connector.apply
        self.perms_collection = Permissions().mongo_connector.apply
        self.user_collection = User().mongo_connector.apply
        self.user_role_map_coll = UserRolesRel().mongo_connector.apply
        self.user_sites_coll = UserSitesRel().mongo_connector.apply

    def change_password(self, data_dict, user_id):
        if data_dict['newPassword'] != data_dict['confirmNewPassword']:
            return {'error': 'password not mathcing'}, 412

        user = self.user_collection.find_one(
            {'email': data_dict['email'], 'user_id': user_id})

        if data_dict['oldPassword'] != user['password']:
            return {'error': 'old password not mathcing'}, 412

        self.user_collection.update(
            {'user_id': user_id},
            {
                '$set': {'password': data_dict['newPassword']}
            }
        )
        return {'updated': True}

    def create_role(self, data_dict):
        role_id = get_next_sequence('role')
        data_dict['id'] = role_id
        self.roles_collection.insert(data_dict)
        return{'recored': True, 'payload': data_dict}

    def create_perms(self, data_dict):
        perm_id = get_next_sequence('perm')
        data_dict['id'] = perm_id
        self.perms_collection.insert(data_dict)
        return{'recored': True, 'payload': data_dict}

    def get_perms(self, _filers):
        mongo_query = {}
        if 'id' in _filers:
            mongo_query['id'] = {'$in': _filers.get('id').split(',')}

        perms = self.perms_collection.find(mongo_query, {'_id': 0})

        return {'data': list(perms)}

    def get_users(self, _filers):
        mongo_query = {
            '$and': [
            ],
            '$or': [
            ]
        }

        for item in _filers.items():
            mongo_query['$and'].append(
                {item[0]: {'$in': item[1].split(',')}}
            )

        for key in mongo_query.keys():
            if not len(mongo_query[key]):
                del mongo_query[key]

        if mongo_query:
            users = self.user_collection.find(
                mongo_query, {'_id': 0, 'password': 0})
        else:
            users = all_users.values()
        users = map(self.get_user_roles, users)

        return {'data': list(users)}

    def get_user_roles(self, user):
        user['roles'] = []
        for role in self.user_role_map_coll.find({'user_id': user['user_id']}):
            user['roles'].append(all_roles[role['role_id']])
        return user

    def get_roles(self, _filers):
        mongo_query = {}
        if _filers.get('id'):
            mongo_query['id'] = {'$in': _filers.get('id').split(',')}

        roles = self.roles_collection.find(mongo_query, {'_id': 0})

        response = []

        for role in roles:
            role['permissions'] = self.get_perms(
                {'id': ','.join(role.get('permissions', []))}
            )['data']
            response.append(role)

        return {'data': response}

    def assign_perms_roles(self, data_dict):
        role_id = data_dict['id']
        perms = data_dict['permissions']
        self.roles_collection.update(
            {'id': role_id},
            {'$set': {'permissions': perms}}
        )

        return {
            'msg': 'Role updated successfully'
        }

    def delete_perms(self, _filers):
        self.perms_collection.delete_many(
            {'id': {'$in': _filers.get('id').split(',')}})

        for role in self.get_roles({})['data']:
            if _filers['id'] in role['permissions']:
                role['permissions'].pop(
                    role['permissions'].index(_filers['id'])
                )
                self.roles_collection.update(
                    {'id': role['id']},
                    {'$set':
                     {'permissions': role['permissions']}
                     }
                )

        return {'recored': True}

    def delete_role(self, _filers):
        self.roles_collection.delete_many(
            {'id': {'$in': _filers.get('id').split(',')}})
        self.user_role_map_coll.delete_many(
            {'role_id': {'$in': _filers.get('id').split(',')}})
        return {'recored': True}

    def assign_user_access(self, data_dict):
        self.user_role_map_coll.delete_many({'user_id': data_dict['user_id']})
        for role in data_dict['roles']:
            self.user_role_map_coll.insert(
                {
                    'user_id': data_dict['user_id'],
                    'role_id': role
                }
            )

        self.user_collection.update(
            {'user_id': data_dict['user_id']},
            {'$set':
             {'sites': data_dict['sites']}
             }
        )

        return {'recored': True}

    def update_user_access(self, data_dict):
        self.user_role_map_coll.delete_many({'user_id': data_dict['user_id']})
        for role in data_dict['roles']:
            self.user_role_map_coll.insert(
                {
                    'user_id': data_dict['user_id'],
                    'role_id': role
                }
            )

        self.user_collection.update(
            {'user_id': data_dict['user_id']},
            {'$set':
             {
                 'sites': data_dict['sites']
             }
             }
        )
        return {'recored': True}

    def get_user_perms(self, user_id):
        roles = [_role['role_id']
                 for _role in self.user_role_map_coll.find({'user_id': user_id})]

        perms = []
        for _role in self.get_roles({'id': ','.join(roles)})['data']:
            for p in _role.get('permissions', []):
                if p['name'] not in perms:
                    perms.append(p['name'])

        return perms
