import traceback

from ..utils.http_status import send_response
from ..models.employees import Employee as EmployeeORM


class Employees:
    def __init__(self):
        self.employee_collection = EmployeeORM().mongo_connector.apply

    def create_employee(self, data, site_id):
        # data_dict["siteId"] = site_id
        # data_dict["first_name"] = first_name
        # data_dict["last_name"] = last_name
        # data_dict["email"] = email
        # data_dict["phone"] = phone
        # data_dict["address1"] = address1
        # data_dict["address2"] = address2
        # data_dict["city"] = city
        # data_dict["state"] = state
        # data_dict["pincode"] = pincode
        # data_dict["designation"] = designation
        # data_dict["department"] = department
        # data_dict["is_admin"] = is_admin
        # data_dict["employee_id"] = employee_id
        # data_dict["aadhar"] = aadhar
        # data_dict["pan"] = pan
        # data_dict["doj"] = doj
        # data_dict["dob"] = dob

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
