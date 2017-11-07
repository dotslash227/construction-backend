from ..caching.cache_handler import CacheDriver
from functools import wraps
from helpers import send_response
import json

def cache_response(expiry_time=1*24*60*60):
  """
  Caches response;
  Returns already cached response if not expired;

  """
  def wrapping(f):
   @wraps(f)
   def wrapped(request, *args, **kwargs):
     if request.headers.get("Cache-Control", "") == "no-cache":
       return f(request, *args, **kwargs)

     cache_obj = CacheDriver()
     cache_key = {
       "path": request.path,
       "method": request.method,
       "body": request.body,
       "params": request.params,
       "user_id": request.user['user_id']
     }
     response = cache_obj.get_cached_data(cache_key)
     if response:
       return send_response((json.loads(response), 200, [("Cache", "HIT")]))
     else:
       response = f(request, *args, **kwargs)
       if response.status_code == 200:
         cache_obj.cache_data(key=cache_key,
                              value=response.json_body,
                              expiry_time=expiry_time,
                              user_id=request.user['user_id'])
         response.headers.extend({"Cache": "MISS"})
       return response
   return wrapped
  return wrapping
