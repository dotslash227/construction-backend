import traceback

from ..utils.http_status import send_response
from pyramid.view import view_config

from ..handlers.supplier_handler import Supplier



@view_config(route_name='supplier')
def supplier(request):
    '''
    /supplier
    '''

    try:
        site_id = request.matchdict['site']
        handler_obj = Supplier()
        if request.method == 'POST':
            response = handler_obj.create_supplier(
                data_dict=request.json_body, site_id=site_id)
            return send_response(response, 200)
        elif request.method == 'GET':
            response = handler_obj.get_suppliers(
                _filers=request.params, site_id=site_id)
            return send_response(response, 200)
        elif request.method == 'PUT':
            response = handler_obj.update_supplier(request.json_body)
            return send_response(response, 200)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)


@view_config(route_name='supplier_retrospective')
def supplier_retrospective(request):
    '''
    /supplier/retrospective
    '''

    try:
        handler_obj = Supplier()

        if request.method == 'PUT':
            response = handler_obj.update_retrospective_changes(
                request.json_body, request.user)
            return send_response(response, 200)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)


