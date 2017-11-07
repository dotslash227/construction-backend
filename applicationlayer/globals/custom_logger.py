import os
import logging
import logging.handlers


class FileLogger:
  """docstring for FileLogger"""
  def __init__(self, logger_name, file_name=None, is_access=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if not file_name:
      file_name = 'applog'

    file_name += ".log"

    # create logs directory if not available
    if not os.path.exists("applicationlayer/logs/"):
      os.makedirs("applicationlayer/logs/")

    fh = logging.handlers.TimedRotatingFileHandler("applicationlayer/logs/" + file_name, when='W0', utc=True)

    if is_access:
      fh.setLevel(logging.INFO)
    else:
      fh.setLevel(logging.DEBUG)

    pid = os.getpid()

    formatter = logging.Formatter("PID: " + str(pid) + " > %(asctime)s - %(name)s - %(levelname)s - [%(module)s - "
                                                       "%(funcName)20s()] - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    self.logger = logger

  def get_logger(self):
    return self.logger


access_logger = FileLogger(logger_name='access', file_name='access', is_access=True).get_logger()
custom_logger = FileLogger(logger_name='custom').get_logger()
response_logger = FileLogger(logger_name='response', file_name='responses', is_access=False).get_logger()
user_logger = FileLogger(logger_name='user', file_name='user_activity', is_access=False).get_logger()
