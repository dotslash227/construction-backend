import traceback
from ..utils.http_status import send_response
from pyramid.view import view_config
from ..handlers.product_handler import Product


@view_config(route_name='product')
def product(request):
    '''
    /product
    '''

    try:
        site_id = request.matchdict['site']
        handler_obj = Product()
        if request.method == 'POST':
            response = handler_obj.create_products(request.json_body, site_id)
            return send_response(response, 200)
        elif request.method == 'GET':
            response = handler_obj.get_products(request.params, site_id)
            return send_response(response, 200)
        elif request.method == 'DELETE':
            response = handler_obj.delete_product(request.params['prodId'])
            return send_response(response, 200)
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)

@view_config(route_name='mixture')
def mixture(request):
    '''
    /product
    '''

    try:
        site_id = request.matchdict['site']
        handler_obj = Product()
        if request.method == 'POST':
            response = handler_obj.create_mixture(request.json_body, site_id)
            return send_response(response, 200)
        elif request.method == 'PUT':
            response = handler_obj.edit_mixture(request.json_body, site_id)
            return send_response(response, 200)
        
        else:
            return send_response(code=405)
    except Exception as e:
        traceback.print_exc()
        return send_response(e.message, 500)