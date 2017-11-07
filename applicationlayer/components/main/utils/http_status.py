status = {
    100: {
        'message': 'Continue',
        'status_type': 'Informational'},
    101: {
        'message': 'Switching Protocols',
        'status_type': 'Informational'},
    200: {
        'message': 'OK',
        'status_type': 'Successful'},
    201: {
        'message': 'Created',
        'status_type': 'Successful'},
    202: {
        'message': 'Accepted',
        'status_type': 'Successful'},
    203: {
        'message': 'Non-Authoritative Information',
        'status_type': 'Successful'},
    204: {
        'message': 'No Content',
        'status_type': 'Successful'},
    205: {
        'message': 'Reset Content',
        'status_type': 'Successful'},
    206: {
        'message': 'Partial Content',
        'status_type': 'Successful'},
    300: {
        'message': 'Multiple Choices',
        'status_type': 'Redirection'},
    301: {
        'message': 'Moved Permanently',
        'status_type': 'Redirection'},
    302: {
        'message': 'Found',
        'status_type': 'Redirection'},
    303: {
        'message': 'See Other',
        'status_type': 'Redirection'},
    304: {
        'message': 'Not Modified',
        'status_type': 'Redirection'},
    305: {
        'message': 'Use Proxy',
        'status_type': 'Redirection'},
    307: {
        'message': 'Temporary Redirect',
        'status_type': 'Redirection'},
    400: {
        'message': 'Bad Request',
        'status_type': 'Client Error'},
    401: {
        'message': 'Unauthorized',
        'status_type': 'Client Error'},
    402: {
        'message': 'Payment Required',
        'status_type': 'Client Error'},
    403: {
        'message': 'Forbidden',
        'status_type': 'Client Error'},
    404: {
        'message': 'Not Found',
        'status_type': 'Client Error'},
    405: {
        'message': 'Method Not Allowed',
        'status_type': 'Client Error'},
    406: {
        'message': 'Not Acceptable',
        'status_type': 'Client Error'},
    407: {
        'message': 'Proxy Authentication Required',
        'status_type': 'Client Error'},
    408: {
        'message': 'Request Timeout',
        'status_type': 'Client Error'},
    409: {
        'message': 'Conflict',
        'status_type': 'Client Error'},
    410: {
        'message': 'Gone',
        'status_type': 'Client Error'},
    411: {
        'message': 'Length Required',
        'status_type': 'Client Error'},
    412: {
        'message': 'Precondition Failed',
        'status_type': 'Client Error'},
    413: {
        'message': 'Request Entity Too Large',
        'status_type': 'Client Error'},
    414: {
        'message': 'Request-URI Too Long',
        'status_type': 'Client Error'},
    415: {
        'message': 'Unsupported Media Type',
        'status_type': 'Client Error'},
    416: {
        'message': 'Requested Range Not Satisfiable',
        'status_type': 'Client Error'},
    417: {
        'message': 'Expectation Failed',
        'status_type': 'Client Error'},
    500: {
        'message': 'Internal Server Error',
        'status_type': 'Server Error'},
    501: {
        'message': 'Not Implemented',
        'status_type': 'Server Error'},
    502: {
        'message': 'Bad Gateway',
        'status_type': 'Server Error'},
    503: {
        'message': 'Service Unavailable',
        'status_type': 'Server Error'},
    504: {
        'message': 'Gateway Timeout',
        'status_type': 'Server Error'},
    505: {
        'message': 'HTTP Version Not Supported',
        'status_type': 'Server Error'}
}


from applicationlayer.utils.helpers import send_response as applicationlayer_send_response


def send_response(message=None, code=200):
    if message in [None]:
        return applicationlayer_send_response((status[code], code))
    elif isinstance(message, tuple):
        return applicationlayer_send_response(message)
    else:
        return applicationlayer_send_response((message, code))
