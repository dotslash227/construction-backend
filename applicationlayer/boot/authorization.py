from jose.jwt import JWTError, encode
from applicationlayer.utils.config import SECRET_KEY
from applicationlayer.utils.helpers import redis_client, parse_token, get_data_from_redis, redis_client_sessions
from pyramid.events import subscriber, ContextFound
from pyramid.httpexceptions import HTTPForbidden, HTTPUnauthorized, HTTPNotFound
import json
import traceback
from datetime import datetime, timedelta
from ..utils.exceptions import SessionExpired

import os


JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 86400


def create_token(user_data):
    payload = {
        'sub': json.dumps(user_data),
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        'lout': False,
        'iat': datetime.utcnow()
    }
    token = encode(payload, SECRET_KEY, JWT_ALGORITHM)
    return token


def generate_token(user_data, features):
    token = create_token(user_data)
    store_in_redis(user_data['user_id'], features)
    return token


@subscriber(ContextFound)
def check(event):
    if not event.request.matched_route:
        raise HTTPNotFound('Not Found')

    # TODO: Need to put this check at appropriate place
    auth_excluded_list = ['login', 'test', 'ticket_print', 'media',
                          'diesel_voucher_print', 'payout_print', 'print_receipt']
    if event.request.matched_route.name not in auth_excluded_list:
        if os.environ.get('local', False):
            event.request.user = {'user_id':'user_3'}
            return True
        if not ('export_token' in event.request.params or 'token' in event.request.matchdict or (
                event.request.headers.get('Authorization') and event.request.headers.get('Authorization').strip() !=
                'Authorization')):
            return 0
            raise HTTPUnauthorized('Missing Authorization Headers')

        try:
            payload = json.loads(parse_token(event.request)['sub'])
            if is_authorised_user(event.request):
                event.request.user = payload
            else:
                raise HTTPForbidden('Forbidden')
        except JWTError as e:
            traceback.print_exc()
            raise HTTPForbidden(e.message)
        except SessionExpired as e:
            raise HTTPUnauthorized(e.message)
        except Exception as e:
            traceback.print_exc()
            raise HTTPForbidden(e.message)


def is_authorised_user(request):

    features = get_data_from_redis(request)
    if not isinstance(features, list):
        raise SessionExpired("Session Timed out")
    current = redis_client.hget(
        'features', request.matched_route.name + ':' + request.method)
    if (not current) or current == 0 or current in features:
        return True
    else:
        return False


def destroy_token(token):
    redis_client.expire(token, 0)


def store_in_redis(user_id, features):
    redis_client_sessions.setex(user_id, 600, '@'.join(features))
