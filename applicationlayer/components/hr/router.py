
class Router:
    def __init__(self):
        pass


    @staticmethod
    def get_routes():
        return [
            {
                'pattern': '{site}/hr/store-employee',
                'name': 'employeeStore'
            },
            {
                'pattern': '{site}/hr/list-all',
                'name': 'listAll'
            }
        ]
