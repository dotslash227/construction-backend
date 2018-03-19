
class Router:
    def __init__(self):
        pass


    @staticmethod
    def get_routes():
        return [
            {
                'pattern': '{site}/hr/employees',
                'name': 'employees'
            },
            {
                'pattern': '{site}/hr/employees/{eid}',
                'name': 'employee-single'
            }
        ]
