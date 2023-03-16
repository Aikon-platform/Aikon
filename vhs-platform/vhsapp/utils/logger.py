import logging
import os
import time

from vhsapp.utils.paths import LOG_PATH, MEDIA_PATH, BASE_DIR
from vhs.settings import DEBUG
from vhsapp.utils.constants import (
    APP_NAME,
)


class TerminalColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_color(msg_type=None):
    if msg_type == "error":
        return TerminalColors.FAIL
    if msg_type == "warning":
        return TerminalColors.WARNING
    return TerminalColors.OKBLUE


# def get_logger(log_dir, name):
#     # log_dir = coerce_to_path_and_check_exist(log_dir)
#     logger = logging.getLogger(name)
#     file_path = log_dir / "{}.log".format(name)
#     hdlr = logging.FileHandler(file_path)
#     formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
#     hdlr.setFormatter(formatter)
#     logger.addHandler(hdlr)
#     logger.setLevel(logging.INFO)
#     return logger


def log(msg):
    """
    Record an error message in the system log
    """
    import logging

    if not os.path.isfile(LOG_PATH):
        f = open(LOG_PATH, "x")
        f.close()

    # Create a logger instance
    logger = logging.getLogger(APP_NAME)
    logger.error(f"{get_time()}\n{msg}")


def console(msg="🚨🚨🚨", msg_type=None):
    if not DEBUG:
        return

    msg = f"\n\n\n{get_time()}\n{get_color(msg_type)}{TerminalColors.BOLD}{msg}{TerminalColors.ENDC}\n\n\n"

    logger = logging.getLogger("django")
    if msg_type == "error":
        logger.error(msg)
    elif msg_type == "warning":
        logger.warning(msg)
    else:
        logger.info(msg)
