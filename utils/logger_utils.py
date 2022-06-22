import logging
import os
from datetime import datetime
from os.path import exists

FILE_TIMESTAMP_FMT = '%Y-%m-%dT%H-%M-%S'
TIMESTAMP_FMT = '%Y-%m-%d %H:%M:%S'

LOG_PATH = os.path.join(os.path.abspath(os.curdir), 'apilogs')
if not exists(LOG_PATH):
    os.mkdir(LOG_PATH)


def get_api_logger():
    logging.basicConfig(filename=f'apilogs/LOG-{datetime.strftime(datetime.now(), FILE_TIMESTAMP_FMT)}.log',
                        filemode='w',
                        level='DEBUG',
                        format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt=TIMESTAMP_FMT)
