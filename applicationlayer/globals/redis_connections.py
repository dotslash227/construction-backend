from .initiate_db_connections import initiate_redis_connection as pool
import redis

redis_pool = pool()


class RedisConnections(object):

  def __init__(self, connection_pool=redis_pool):
    self._redis_connection = redis.StrictRedis(connection_pool=connection_pool)

  @property
  def redis_connection(self):
    return self._redis_connection
