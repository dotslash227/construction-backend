import traceback

from ..utils.http_status import send_response
from pyramid.view import view_config

from ..handlers.acl_handler import ACL


@view_config(route_name='permission')
def permissions(request):
    '''
    /permission
    '''

    try:
        handler_obj = ACL()
        if request.method == 'POST':
            response = handler_obj.create_perms(request.json_body)
            return send_response(response, 200)
        elif request.method == 'GET':
            response = handler_obj.get_perms(request.params)
            return send_response(response, 200)
        elif request.method == 'DELETE':
            response = handler_obj.delete_perms(request.json_body)
            return send_response(response, 200)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)


@view_config(route_name='role')
def role(request):
    '''
    /role
    '''

    try:
        handler_obj = ACL()
        if request.method == 'POST':
            response = handler_obj.create_role(request.json_body)
            return send_response(response, 200)
        elif request.method == 'GET':
            response = handler_obj.get_roles(request.params)
            return send_response(response, 200)
        elif request.method == 'DELETE':
            response = handler_obj.delete_role(request.json_body)
            return send_response(response, 200)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)


@view_config(route_name='role_permission')
def role_permission(request):
    '''
    /role/permission
    '''

    try:
        handler_obj = ACL()
        if request.method == 'POST':
            response = handler_obj.assign_perms_roles(request.json_body)
            return send_response(response, 200)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)


@view_config(route_name='change_password')
def change_password(request):
    '''
    /changePassword
    '''

    try:
        handler_obj = ACL()
        if request.method == 'POST':
            response = handler_obj.change_password(
                request.json_body, request.user['user_id'])
            return send_response(response)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)


@view_config(route_name='user_access_map')
def user_access_map(request):
    '''
    /user/access
    '''

    try:
        handler_obj = ACL()
        if request.method == 'POST':
            response = handler_obj.assign_user_access(request.json_body)
            return send_response(response, 200)
        if request.method == 'PUT':
            response = handler_obj.update_user_access(request.json_body)
            return send_response(response, 200)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)
