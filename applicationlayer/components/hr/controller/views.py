import traceback

from ..utils.http_status import send_response
from pyramid.view import view_config
from ..handlers.EmployeeHandler import Employees


@view_config(route_name="employees")
def employees(request):
    employee_obj = Employees()
    site_id = request.matchdict["site"]
    if request.method == "POST":
        response = employee_obj.create_employee(request.json_body, site_id)
        return send_response(response, 200)
    if request.method == "GET":
        response = employee_obj.all_employees(site_id)
        return send_response(response, 200)


@view_config(route_name="employee-single")
def employeeSingular(request):
    employee_obj = Employees()
    site_id = request.matchdict["site"]
    eid = request.matchdict["eid"]
    if request.method == "GET":
        response = employee_obj.get_employee(site_id, eid)
        return send_response(response, 200)
    if request.method == "DELETE":
        response = employee_obj.delete_employee(site_id, eid)
        return send_response(response, 200)
