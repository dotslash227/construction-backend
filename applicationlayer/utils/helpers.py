from pyramid.view import notfound_view_config
from pyramid.response import Response
import json
import os
from datetime import datetime
import traceback
from bson.objectid import ObjectId
from cgi import FieldStorage
from functools import wraps
from .mysql_helper import MYSQLQueryUtils
from ..globals.redis_connections import RedisConnections
from applicationlayer.utils.config import SECRET_KEY
from jose.jwt import decode
from applicationlayer.globals.initiate_db_connections import initiate_redis_connection
from exceptions import SessionExpired

from ..models.sequence import Counters

mysql_utils = MYSQLQueryUtils()

redis_client = RedisConnections().redis_connection
session_pool = initiate_redis_connection(db=1)
redis_client_sessions = RedisConnections(
    connection_pool=session_pool).redis_connection
cache_pool = initiate_redis_connection(db=2)
redis_cache = RedisConnections(connection_pool=cache_pool).redis_connection

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
json_headers = ('content-type', 'application/json')

type_definition = {
    'string': ["contains", "not contains", "begins with", "ends with", "equals", "not equals"],
    'date': ["Before", "After", "On"],
    'number': ['Less Than', 'More Than', 'Equals'],
    'boolean': ['Equals', 'Not Equals']
}


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, FieldStorage):
            return str(o)
        return json.JSONEncoder.default(self, o)


def send_response(response):
    if isinstance(response, tuple):
        return Response(body=JSONEncoder().encode(response[0]), status=response[1], content_type='application/json',
                        headerlist=response[2] if len(response) > 2 else [json_headers])
    else:
        return Response(body=JSONEncoder().encode(response), content_type='application/json')


class EmptyException(Exception):

    def __init__(self):
        Exception.__init__(self, 'Data not found')


def get_next_sequence(name):
    counters_collection = Counters().mongo_connector.apply
    seq = counters_collection.find_and_modify(
        query={name: {'$exists': True}},
        update={'$inc': {name: 1}},
        new=True
    ).get(name)
    return name + '_' + str(seq)


def extract_token(request):
    return request.headers.get('Authorization').split()[1] if 'Authorization' in request.headers else (
        request.params['export_token'] if 'export_token' in request.params else (
            request.matchdict['token'] if 'token' in request.matchdict else ''))


def parse_token(req):

    token = req.headers.get('Authorization').split()[1] if 'Authorization' in req.headers else (
        req.params['export_token'] if 'export_token' in req.params else (
            req.matchdict['token'] if 'token' in req.matchdict else ''))
    return decode(token, SECRET_KEY, algorithms=['HS256'])


def get_data_from_redis(request):
    user_id = json.loads(parse_token(request)['sub'])['user_id']
    try:
        features = 'admin.can_audit@strategy.can_view@user.can_dubuque_data@datastats.can_view@menu.can_measure_builder@dataflow.can_create@admin.can_dataflow@menu.can_admin@admin.can_platform_config@source.can_create@health_module.can_assign@ccm.can_view@roles.can_view@menu.can_worksets@admin.can_group_management@measure_builder.can_create@pipeline.can_view@user.can_dubuque_phi_data@patient.can_manual_entry@user.is_north_iowa_user@admin.can_role_management@staff_workqueue.can_access@user.can_clinton_data@workset.can_export@user.is_siouxland_user@dashboard.can_share@source.can_view@roles.can_create@menu.can_sources@groups.can_view@menu.can_dashboard_menu@user.can_central_iowa_phi_data@users.can_view@work_queue.can_create@pipeline.can_create@patient.can_view_profile@hcpa.can_view@measure.can_view@user.can_north_iowa_phi_data@ccm.can_assign@user.is_central_iowa_user@health_module.can_view@menu.can_dataflow_management@menu.can_dashboard_builder@workset.cannot_phi@users.can_phi@dashboard.can_create@user.can_siouxland_data@workset.can_create@user.is_clinton_user@groups.can_create@user.can_siouxland_phi_data@admin.can_user_management@patient.can_search@work_queue.can_view@measure.can_list_patients@users.can_resetpassword@user.can_north_iowa_data@menu.can_group_management@menu.can_role_management@workset.can_share@dataflow.can_view@menu.can_measures@user.is_dubuque_user@dashboard.can_view@measure_builder.can_view@menu.can_user_management@user.can_clinton_phi_data@ccm.can_call@workset.can_view@users.can_create@user.can_central_iowa_data'.split(
            '@')
        # redis_client_sessions.expire(user_id, 600)
    except Exception as e:
        print e
        raise SessionExpired('User Session Expired')
    return features


def parse_date(unparsed_date):

    b_date_epoch = '0'
    try:
        if unparsed_date:
            if unparsed_date.isdigit():
                unparsed_date = str(unparsed_date)
                b_date_epoch = datetime.strptime(
                    unparsed_date, '%Y%m%d').strftime('%s')
            else:
                unparsed_date = unparsed_date[:10]
                b_date_epoch = datetime.strptime(
                    unparsed_date, '%Y-%m-%d').strftime('%s')
    except Exception:
        print "\n unparsed_date " + str(unparsed_date) + " does not follow expected format (yyyy-mm-dd). setting age = 0.\n"
    return int(b_date_epoch)


def calculate_age(dob, dod=''):

    dob = parse_date(dob)
    if dod:
        max_epoch = parse_date(dod)
    else:
        max_epoch = int(datetime.utcnow().strftime('%s'))
    age = (max_epoch - dob) / (86400 * 365)
    return age if age >= 0 else 0


def get_user_data(user_id):
    user_data_query = 'select first_name,last_name,email from users where user_id = "' + user_id + '"'
    userinfo = mysql_utils.get_data(user_data_query)[0]
    return userinfo


def get_authorised_users_for_chapter_data(request, chapter_code=None):
    permissions_collection = Permissions().mongo_connector.apply
    group_collection = Group().mongo_connector.apply
    data_permissions = permissions_collection.find_one(
        {
            "name": "data_access",
            "permissions.chapter_code": chapter_code
        },
        {
            "permissions.$": 1
        }
    )
    permission_id = None
    if 'permissions' in data_permissions and len(data_permissions['permissions']) == 1:
        permission_id = data_permissions['permissions'][0]['permission_id']
    role_ids = []
    if permission_id:
        role_query = 'select distinct(role) from role_features where permission = "' + str(
            permission_id) + '"'
        role_ids = mysql_utils.get_data(role_query)
        role_ids = [str(role_id[0]) for role_id in role_ids]
    user_ids = set()
    if role_ids:
        groups = list(group_collection.find(
            {
                'roles': {
                    '$in': role_ids
                }
            },
            {
                'members': 1
            }
        ))
        for group in groups:
            user_ids.update(set([member['user_id']
                                 for member in group['members']]))
    return list(user_ids)


def catch_exception(f):
    """A one point exceptions Handler
        From point of exception do->
            raise Exception(error_message, status_code)

            *Note:status_code: Must be an int*
    """

    @wraps(f)
    def _catch_exc(request, *args, **kwargs):
        try:
            ret = f(request, *args, **kwargs)
            return ret
        except Exception as e:
            traceback.print_exc(e)
            error = e.args[0] if len(e.args) > 0 else 'Error...Retry'
            status = e.args[1] if (
                len(e.args) > 1and isinstance(e.args[1], int)) else 500
            return send_response(({'status': 0, 'error': error}, status))
    return _catch_exc


def matchdict_default(**kw):
    def f(info, request):
        for k, v in kw.iteritems():
            info['match'].setdefault(k, v)
        return True
    return f


@notfound_view_config()
def not_found(request):
    return send_response(('Not found!', 404))


def custom_mapper(my_dict, old_keys, new_keys, keys_len):
    return {new_keys[index]: my_dict[old_keys[index]] for index in range(keys_len)}


def get_current_time():
    cur_timestamp = datetime.utcnow()
    added_on = int(cur_timestamp.strftime("%s")) * 1000 + \
        int(cur_timestamp.microsecond / 1000)
    return added_on
