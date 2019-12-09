import os
import sys

file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)


def config_path():
    home = os.getenv('HOME')
    c_path = home + '/fpvcar/config.json'
    if not os.path.exists(c_path):
        print('failed to find config file in ' + c_path)
        print('see in ../shell/setup for an example')
        sys.exit(1)
    return c_path


def file_delete(file_name):
    if os.path.exists(file_name):
        print('remove ' + file_name)
        os.remove(file_name)
