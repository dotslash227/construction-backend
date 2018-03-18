import traceback

from ..utils.http_status import send_response
from pyramid.view import view_config
from ..handlers.EmployeeHandler import Employees


@view_config(route_name="employeeStore")
def addEmployee(request):
    employee_obj = Employees()
    site_id = request.matchdict["site"]
    if request.method == "POST":
        response = employee_obj.create_employee(request.json_body, site_id)
        return send_response(response, 200)

    return send_response(response)
