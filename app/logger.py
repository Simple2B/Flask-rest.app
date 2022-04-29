import os
import sys
from loguru import logger

LOG_FILE = os.environ.get("LOG_FILE")

log_format = "{time} - {name} - {level} - {message}"
# /var/log/project_name/LOG_FILE
# Change LOG_FILE in .flaskenv to enable or disable (empty) logging to a file
if LOG_FILE:
    logger.add(LOG_FILE, format=log_format, serialize=True,
            level="DEBUG", rotation="1 week", compression="zip", colorize=True)

logger.add(sys.stdout, format=log_format, serialize=True, level="DEBUG", colorize=True)


# Old standart logger. Delete if no use.

'''import logging

LOGGER_NAME = "SimpleAppLog"


class Logger(object):
    # __created_std_out = False
    log_file = bytes
    EXCEPTION = 100
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(self):
        self.__log = logging.getLogger(LOGGER_NAME)
        # create formatter
        formatter = logging.Formatter("%(asctime)-15s [%(levelname)-8s] %(message)s")
        chanel = logging.StreamHandler(sys.stderr)
        chanel.setLevel(logging.DEBUG)
        chanel.setFormatter(formatter)
        self.__log.addHandler(chanel)

        self.__log.setLevel(self.INFO)
        self.__methods_map = {
            self.DEBUG: self.__log.debug,
            self.INFO: self.__log.info,
            self.WARNING: self.__log.warning,
            self.ERROR: self.__log.error,
            self.CRITICAL: self.__log.critical,
            self.EXCEPTION: self.__log.exception,
        }
        self.DEFAULT_LEVEL = self.INFO

    def __call__(self, msg, lvl=None, *args, **kwargs):
        if not lvl:
            self.__log.log(self.DEFAULT_LEVEL, msg, *args, **kwargs)
        elif lvl in self.__methods_map:
            self.__methods_map[lvl](msg, *args, **kwargs)
        else:
            self.__log.log(lvl, msg, *args, **kwargs)

    def set_level(self, level=None):
        if level is None:
            level = self.DEFAULT_LEVEL
        self.__log.setLevel(level)


log = Logger()'''