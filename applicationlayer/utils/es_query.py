import ujson, json
import requests
from ..utils.config import ElasticsearchCredentials
from ..caching.cache_handler import CacheDriver


class ESQuery:
  """Base Class for generating, executing elasticsearch query"""
  __q = {}
  __url_parts = {}

  def __init__(self, logger, url_parts, q_attribs=None, enable_cache=False, expiry_time=24 * 60 * 60):
    self.enable_cache = enable_cache
    self.expiry_time = expiry_time

    url_obj = ElasticsearchCredentials()
    url_defaults = {
      'proto': 'http',
      'host': url_obj.host,
      'port': url_obj.port,
      'index': None,
      'doc_type': None,
      'method': '_search',
      'is_scroll' : False,
      'scroll' : '3m',
      'export': False
    }

    for url_part, part_default in url_defaults.iteritems():
      self.__url_parts[url_part] = url_parts.get(url_part, part_default)

    if q_attribs:
      self.set_q_attribs(q_attribs)

    self.logger = logger

  def set_q_attribs(self, q_attribs):
    if q_attribs.get('is_filtered'):
      self.__q = {
        "query": {
          "filtered": {
            "query": {
              "match_all": {}
            },
            "filter": {}
          }
        }
      }

      if q_attribs.get('filters'):
        self.__q['query']['filtered']['filter'] = q_attribs.get('filters')

      if q_attribs.get('base_query'):
        self.__q['query']['filtered']['query'] = q_attribs.get('base_query')
    else:
      self.__q = {
        "query": {
          "match_all": []
        }
      }
      if q_attribs.get('base_query'):
        self.__q['query'] = q_attribs.get('base_query')

    if q_attribs.get('aggs'):
      self.__q['aggs'] = q_attribs.get('aggs')

  def set_filters(self, filters):
    self.__q['query']['filtered']['filter'] = filters

  def get_filters(self):
    return self.__q['query']['filtered']['filter']

  def set_sort(self, sort_filter=None):
    if sort_filter:
      if 'sort' not in self.__q:
        self.__q['sort'] = []

      if isinstance(sort_filter, list):
        self.__q['sort'].extend(sort_filter)
      else:
        self.__q['sort'].append(sort_filter)

  def get_sort(self):
    return self.__q.get('sort', [])

  def set_aggs(self, aggs):
    self.__q['aggs'] = aggs

  def get_aggs(self):
    if 'aggs' not in self.__q:
      self.__q['aggs'] = {}
    return self.__q['aggs']

  def set_fields(self, fields):
    self.__q['fields'] = fields

  def unset_fields(self):
    if 'fields' in self.__q:
      del self.__q['fields']

  def get_fields(self):
    return self.__q['fields']

  def set_includes(self, fields):
    if '_source' not in self.__q:
      self.__q['_source'] = {}
    self.__q['_source']['includes'] = fields

  def get_includes(self):
    return self.__q['_source']['includes']

  def set_excludes(self, fields):
    if '_source' not in self.__q:
      self.__q['_source'] = {}
    self.__q['_source']['excludes'] = fields

  def get_excludes(self):
    return self.__q['_source']['excludes']

  def set_size(self, size):
    self.__q['size'] = size

  def get_size(self):
    return self.__q['size']

  def set_offset(self, offset):
    self.__q['from'] = offset

  def get_offset(self):
    return self.__q['from']

  def get_url(self):

      url = "{proto}://{host}:{port}/".format(
          proto = self.__url_parts['proto'],
          host = self.__url_parts['host'],
          port = self.__url_parts['port']
      )
      if self.__url_parts['index']:
          url += self.__url_parts['index'] + '/'
          if self.__url_parts['doc_type']:
              url += self.__url_parts['doc_type'] + '/'

      url += self.__url_parts['method']
      if self.__url_parts['is_scroll']:
          url += '?scroll=' + self.__url_parts['scroll']
      elif self.__url_parts['export']:
          url += '/scroll'
      return url


  def set_query(self, q):
    self.__q = q

  def get_query(self):
    return self.__q

  def execute(self, method='GET', log=True):

    url = self.get_url()
    serial_q = json.dumps(self.__q)
    caching_object = CacheDriver()

    if log:
      self.log_query(url, serial_q)

    key = ({'url': url, 'q': serial_q, 'method': method})
    if self.__url_parts['method'] == '_search' and self.enable_cache:
        data = caching_object.get_cached_data(key)
        if data:
            return ujson.loads(data)

    if method.upper() == 'GET':
      r = requests.get(url)
    elif method.upper() == 'POST':
      r = requests.post(url, data=serial_q)
    elif method.upper() == 'PUT':
      r = requests.put(url, data=serial_q)

    if r.status_code / 100 == 2:
        if self.enable_cache and self.__url_parts['method'] == "_search":
          caching_object.cache_data(key, r.json(), self.expiry_time)
        return r.json()
    else:
      raise Exception(r.json())

  def log_query(self, url, serial_q):
    self.logger.debug(url)
    self.logger.debug(serial_q)

  @staticmethod
  def get_data(data, is_count=False):
    if is_count:
      return data['count']
    else:
      rows = []
      hits = data['hits']['hits']
      for hit in hits:
        rows.append(hit['_source'])
      return rows

  @staticmethod
  def get_distinct_values(data, group_field):
    distinct_values = map(lambda x: x['key'], data['aggregations'][group_field]['buckets'])
    return distinct_values
