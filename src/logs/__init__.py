import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

logger.remove()


def hide_pwd_logs(record):
    if 'pwd' in record['message']:
        return False

    return True


logger.add(
    sink=sys.stdout,
    level=os.getenv('LOGGER_LEVEL').upper(),
    filter=hide_pwd_logs
)

logger.add(
    "../var/lib/logs/logs.log",
    level="DEBUG"
)

logger.add(
    "../var/lib/logs/logs-ERROR.log",
    level="ERROR"
)
