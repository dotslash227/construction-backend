from ....models.users import User

import time

from ....boot.authorization import destroy_token
from ....boot.authorization import generate_token
from .acl_handler import ACL
from ..models.sites import Sites


class Login(object):

    def __init__(self, request=None):
        self.request = request
        self.sites_collection = Sites().mongo_connector.apply
        self.user_collection = User().mongo_connector.apply

    def login(self, email, password):
        acl_obj = ACL()
        match = self.user_collection.find_one(
            {'email': email, 'password': password}, {'_id': 0, 'password': 0})
        if not match:
            return {'status': False}
        self.user_collection.update(
            {'email': email, 'password': password},
            {'$set': {
                'lastLogin': time.time() * 1000,
            }
            }
        )
        permissions = acl_obj.get_user_perms(match['user_id'])
        match['sites'] = list(self.sites_collection.find(
            {'id': {'$in': match.get('sites', [])}}, {'_id': 0}))
        token = generate_token(match, permissions)
        match['permissions'] = permissions
        return {
            'status': True,
            'userInfo': match,
            # 'permissions': permissions,
            'authToken': token
        }

    def logout(self, request):
        destroy_token(request.headers.get('Authorization').split()[1])
        return {'loggedOut': True}

    def me(self):
        return self.request.user
