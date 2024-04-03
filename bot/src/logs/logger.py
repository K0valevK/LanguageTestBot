from config import settings
from datetime import datetime
from os import rename
from os.path import getsize

import logging


LOG_FILE_NAME = "{}-{}.tsv"
LOG_FILE_PATH = "./src/logs/log_files/{}"
TIME_FORMAT = "%Y-%m-%d-%H-%M"

log_names = {"user_journey": "user_journey",
             "errors": "errors"}
current_files = {"user_journey": LOG_FILE_NAME.format(datetime.today().strftime(TIME_FORMAT), log_names["user_journey"]),
                 "errors": LOG_FILE_NAME.format(datetime.today().strftime(TIME_FORMAT), log_names["errors"])}
logging_format = {"user_journey": "{log_type} {timestamp} {user_id} {app_ver} {event_group} {event_name} {event_data}",
                  "errors": "{log_type} {timestamp} {user_id} {app_ver} {meta_info} {reason} {category}"}

mapped_stats_key = {"Моя": "mine",
                    "Найти по username": "by_username",
                    "Лидеры": "leaders"}
mapped_test_key = {"По уровню сложности": "leveled",
                   "Бесконечный": "endless"}


# logging.basicConfig(level=logging.INFO, filename=current_file)
open(LOG_FILE_PATH.format(current_files[log_names["user_journey"]]), 'x')
open(LOG_FILE_PATH.format(current_files[log_names["errors"]]), 'x')


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def get_stats_key(key: str):
    return mapped_stats_key[key]


def get_test_key(key: str):
    return mapped_test_key[key]


def check_size(file):
    return (getsize(file) / (1024 * 1024)) > 1


def new_file(log_type):
    rename(LOG_FILE_PATH.format(current_files[log_type]),
           LOG_FILE_PATH.format("_" + current_files[log_type]))
    current_files[log_type] = LOG_FILE_NAME.format(datetime.today().strftime(TIME_FORMAT), log_type)

    open(LOG_FILE_PATH.format(current_files[log_type]), 'x')


def log(log_type, **msg):
    if log_type == "user_journey" and check_size(LOG_FILE_PATH.format(current_files[log_type])):
        new_file(log_type)

    msg = logging_format[log_type].format(log_type=log_type,
                                          app_ver=settings.app_version,
                                          **msg)

    with open(LOG_FILE_PATH.format(current_files[log_type]), 'a') as file:
        print(msg, sep="\n", file=file)
