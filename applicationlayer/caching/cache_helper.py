import zlib
import hashlib
import ujson as json


class CacheHelper(object):
  def compress(self, content, method='zlib'):
    if method == 'zlib':
      try:
        return zlib.compress(str(json.dumps(content)).encode('ascii', 'ignore'))
      except:
        return None

  def decompress(self, content, method='zlib'):
    if method == 'zlib':
      try:
        return zlib.decompress(content)
      except:
        return None

  def hash(self, content):
    return hashlib.md5(str(content)).digest()
