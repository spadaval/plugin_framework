import logging
import os

logger = logging.getLogger()


def init_logger(level=logging.DEBUG, path=None):
    if path is None:
        path = os.path.join(os.getcwd(), "log.txt")

    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = None
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )  # add the handlers to the logger
    try:
        fh = logging.FileHandler(path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception:
        logger.debug("Failed to create log file")
    # create console handler with a provided log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
