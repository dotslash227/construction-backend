import traceback

from ..utils.http_status import send_response
from ..models.employees import Employee as EmployeeORM


class Employees:
    def __init__(self):
        self.employee_collection = EmployeeORM().mongo_connector.apply

    def create_employee(self, data, site_id):

        final_data = {
            "site_id":site_id,
            "eID":data["employee_id"],
            "first_name":data["first_name"],
            "last_name":data["last_name"],
            "email":data["email"],
            "phone":data["phone"],
            "address1":data["address1"],
            "address2":data["address2"],
            "city":data["city"],
            "pin":data["pin"],
            "state":data["state"],
            "designation":data["designation"],
            "department":data["department"],
            "is_admin":data["is_admin"],
            "aadhar":data["aadhar"],
            "pan":data["pan"],
            "doj":data["doj"],
            "dob":data["dob"]
        }

        self.employee_collection.insert(final_data)
        return {'recorded':True,'payload':final_data}

    def all_employees(self, site_id):
        mongo_query = {'site_id':site_id}
        employees = self.employee_collection.find(mongo_query)
        response = list(employees)
        return response

    def get_employee(self, site_id, eid):
        mongo_query = {'site_id':site_id, 'eID':eid}
        employee = self.employee_collection.find(mongo_query)
        response = list(employee)
        return response

    def delete_employee(self, site_id, eid):
        mongo_query = {'site_id': site_id, 'eID':eid}
        employee = self.employee_collection.remove(mongo_query, 'true')
        response = {'deleted':'true'}
        return response
