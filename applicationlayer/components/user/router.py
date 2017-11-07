class Router:

    def __init__(self):
        pass

    @staticmethod
    def get_routes():
        return [
            {
                'pattern': '/permission',
                'name': 'permission'
            },
            {
                'pattern': '/role',
                'name': 'role'
            },
            {
                'pattern': '/role/permissions',
                'name': 'role_permission'
            },
            {
                'name': 'user_access_map',
                'pattern': '/user/access'
            },
            {
                'name': 'users',
                'pattern': '/users'
            },
            {
                'name': 'login',
                'pattern': '/login'
            },
            {
                'name': 'me',
                'pattern': '/me'
            },
            {
                'name': 'change_password',
                'pattern': '/changePassword'
            },
        ]
