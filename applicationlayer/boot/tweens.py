import json
import traceback
from datetime import datetime
from pyramid.response import Response
from authorization import parse_token
from ..globals.custom_logger import access_logger, response_logger, user_logger
from ..utils.helpers import JSONEncoder


response_headers = {
  "Access-Control-Expose-Headers": "WWW-Authenticate, Server-Authorization",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS, PUT, DELETE, PATCH",
  "Access-Control-Allow-Headers": "x-requested-with,content-type,Cache-Control,Pragma,Date,Authorization"
}


def headers_tween_factory(handler, registry):
  def timing_tween(request):
    if request.method != 'OPTIONS':
      log = log_request(request)
      response = handler(request)
      response.headers.extend(response_headers)
      log_response(log, request, response)
      return response
    else:
      return Response(body="", headerlist=response_headers.items())

  return timing_tween


def log_response(log, request, response):
  try:
    user_id = json.loads(parse_token(request).get('sub', '{}')).get('user_id', 'User info not found')
  except Exception:
    user_id = 'User info not found'
  try:
    if request.matched_route.name == 'user_auth':
      if response.status_code / 100 == 2:
        response_body = json.loads(response.body)['status']
      else:
        response_body = json.loads(response.body)['message']
      log_user = '{timestamp} :: {user_id} :: {request_path} :: {response_body} :: {response_status_code} '.format(
        user_id=user_id,
        timestamp=datetime.now(),
        request_path=request.path,
        response_body=response_body,
        response_status_code=response.status_code)

      user_logger.info(log_user)

    if response.status_code / 100 != 2:
      log += ' :: {response_body} :: {response_status_code} :: {cache_status}'.format(
       response_body=response.body,
       response_status_code=response.status_code,
       cache_status=response.headers.get('Cache', 'No Cache'))

      response_logger.info(log)
  except Exception:
    traceback.print_exc()


def log_request(request):
  query_params = {}
  try:
    post_body = request.json_body
  except Exception:
    post_body = {}
  if request.params:
    query_params = request.params

  try:
    user_id = json.loads(parse_token(request).get('sub', '{}')).get('user_id', 'User info not found')
  except Exception:
    user_id = 'User info not found'

  try:
    log = '{host} {timestamp} :: {user_id} :: {method} {path} :: {query_params} :: {post_body} :: {client_addr} ' \
          '{user_agent}'.format(
      user_id=user_id,
      timestamp=datetime.utcnow().strftime('%s'),
      url=request.url,
      body=request.body,
      post_body=post_body,
      query_params=JSONEncoder().encode(dict(query_params)),
      path=request.path,
      host=request.host,
      user_agent=request.user_agent,
      client_addr=request.client_addr,
      method=request.method)

    access_logger.info(log)
    return log
  except Exception:
    request.custom_logger.error("Failed logging incoming request")
    traceback.print_exc()
