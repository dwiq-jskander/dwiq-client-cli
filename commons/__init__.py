import logging
import os

import google.cloud.logging
from pydantic import BaseModel


class LoggingEnvironment(BaseModel):
    name: str = os.environ.get("APP_NAME", "dwiq-client-cli")
    level: str = os.environ.get("LOGGING_LEVEL", "DEBUG")
    type: str = os.environ.get("LOGGING_TYPE", "cloud")
    date_format: str = os.environ.get("LOGGING_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
    format: str = os.environ.get(
        "LOGGING_FORMAT", "%(asctime)s %(levelname)s --- %(message)s"
    )


env = LoggingEnvironment()


def get_logger() -> logging.Logger:
    # Instantiates a client
    if env.type == "cloud":
        # use cloud version to have proper log type (INFO, DEBUG, ERROR) tagging
        # otherwise, a streamed logger will have a type of 'default'
        client = google.cloud.logging.Client()  # type: ignore

        # at INFO level and higher
        client.setup_logging()  # type: ignore
        logger = logging.getLogger()
        logger.setLevel(env.level)
    else:
        # Now create a stream logger and add the handler:
        # When running under pytest, the configuration
        # `pyproject.toml`/tool.pytest.ini_options is used and the following is ignored
        logger = logging.getLogger(env.name)
        formatter = logging.Formatter(env.format, env.date_format)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.setLevel(env.level)
        logger.addHandler(stream_handler)
    return logger


logger = get_logger()
