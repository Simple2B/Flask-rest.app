import os
import sys
from loguru import logger

LOG_FILE = os.environ.get("LOG_FILE")

log_format = "{time} - {name} - {level} - {message}"
# /var/log/project_name/LOG_FILE
# Change LOG_FILE in .flaskenv to enable or disable (empty) logging to a file
if LOG_FILE:
    logger.add(
        LOG_FILE,
        format=log_format,
        serialize=True,
        level="DEBUG",
        rotation="1 week",
        compression="zip",
        colorize=True
    )

logger.add(sys.stdout, format=log_format, serialize=True, level="DEBUG", colorize=True)
