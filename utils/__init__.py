from json import dumps as dump_json_data
from json import loads as load_json_data
from os import listdir, remove

from metaopt.settings.environment import BASE_DIR


def delete_logs():
    for file in listdir(BASE_DIR):
        if '.log' in file:
            remove(file)