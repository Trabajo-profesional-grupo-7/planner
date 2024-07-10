import logging

logger = logging.getLogger(__name__)


def default_logging_config():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )


def get_logger():
    return logging.getLogger(__name__)
