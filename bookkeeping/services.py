from configparser import ConfigParser
import os
import pkg_resources
import sqlite3
import shutil

from .helpers import user_config_dir, user_data_dir

__all__ = (
    'make_config',
    'make_default_config',
    'make_connection',
)


def make_config(*config_files):
    config = ConfigParser()
    config.read(config_files)
    return config


def make_default_config():
    """Читает конфигурационный файл по-умолчанию."""
    filename = os.path.join(user_config_dir, 'config.ini')
    if not os.path.exists(filename):
        default = pkg_resources.resource_filename(
            __name__, 'resources/config.ini'
        )
        print(os.path.exists(default))
        shutil.copyfile(default, filename)  # cp
    return make_config(filename)


config = make_default_config()


def make_connection(name='db'):
    """
    Возвращает объект-подключения к БД SQLite.
    """
    db_name = os.path.join(user_data_dir, config.get(name, 'db_name'))
    conn = sqlite3.connect(
        db_name, detect_types=sqlite3.PARSE_DECLTYPES
    )
    conn.row_factory = sqlite3.Row
    return conn
