import traceback

from ..utils.http_status import send_response
from pyramid.view import view_config
# from ..handler.login_handler import Login
from applicationlayer.components.user.handlers.acl_handler import ACL
from applicationlayer.components.user.handlers.login_handler import Login


@view_config(route_name='login')
def login(request):
    try:
        login_obj = Login()
        if request.method == 'POST':
            if ('email' not in request.json_body) or ('password' not in request.json_body):
                return send_response(code=400)
            response = login_obj.login(
                request.json_body['email'], request.json_body['password'])
            if not response.get('status'):
                return send_response(code=401)
            else:
                return send_response(response)
        elif request.method == 'DELETE':
            response = login_obj.logout(request)
            return send_response(response)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)


@view_config(route_name='me')
def me(request):
    try:
        login_obj = Login(request)
        if request.method == 'GET':
            response = login_obj.me()
            return send_response(response)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)


@view_config(route_name='users')
def users(request):
    try:
        login_obj = ACL()
        if request.method == 'GET':
            response = login_obj.get_users(request.params)
            return send_response(response)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)
