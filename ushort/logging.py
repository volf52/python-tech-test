import logging
import sys

from gunicorn.glogging import Logger
from loguru import logger

LOG_LEVEL = logging.getLevelName("INFO")
JSON_LOGS = False


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_log = logging.getLogger("gunicorn.error")
        self.access_log = logging.getLogger("gunicorn.access")

        self.error_log.addHandler(handler)
        self.access_log.addHandler(handler)

        self.error_log.setLevel(LOG_LEVEL)
        self.access_log.setLevel(LOG_LEVEL)


def configure_logger_for_gunicorn():
    intercept_handler = InterceptHandler()
    logging.root.setLevel(LOG_LEVEL)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])


def configure_logger_for_uvicorn():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])
