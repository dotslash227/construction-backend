from ..globals.custom_logger import custom_logger


class LogExceptions:
  def __init__(self):
    pass

  @staticmethod
  def log_exception(message):
    print message
    custom_logger.exception(message)
