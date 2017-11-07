from applicationlayer.utils.helpers import redis_cache
from cache_helper import CacheHelper

status_code = {
  "success" : 1,
  "failure" : 0
}


class CacheDriver(object):
  def __init__(self):
    self.redis_conn = redis_cache
    self.cacheHelper = CacheHelper()

  def cache_data(self, key, value, expiry_time=24*60*60, user_id=''):
    # get key, value and expiry time(optional) to cache in redis
    # return 1 for success, 0 for failure
    # expiry time is in seconds
    try:
      hashed_key = self.cacheHelper.hash(key)
      compressed_value = self.cacheHelper.compress(value)
      self.redis_conn.set(hashed_key, compressed_value)
      self.redis_conn.expire(hashed_key, time=expiry_time)
      if user_id:
        self.redis_conn.lpush("cache:"+user_id, hashed_key)

      return status_code['success']
    except:
      return status_code['failure']


  def get_cached_data(self, key):
    # return cached data if present for a given key
    # return data for success, None for failure

    hashed_key = self.cacheHelper.hash(key)
    temp = self.redis_conn.get(hashed_key)
    if temp:
      decompressed = self.cacheHelper.decompress(temp)
      return decompressed
    else:
      return None

  def clear_cache(self, key=None):
    # clear cache for key if given, otherwise all
    if key:
      hashed_key = self.cacheHelper.hash(key)
      self.redis_conn.expire(hashed_key, 0)
    else:
      self.redis_conn.flushall()

  def clear_user_cache(self, user_id):
    # clear cache for given user
    keys = self.redis_conn.lrange("cache:"+user_id, 0, -1)
    self.redis_conn.delete(keys)
    self.redis_conn.delete("cache:"+user_id)
