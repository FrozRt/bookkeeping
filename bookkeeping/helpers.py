from datetime import datetime
import os
import appdirs
from prettytable import PrettyTable

_all_ = (
    'prompt',
    'input_date',
    'input_datetime',
    'print_table',
    'user_config_dir',
    'user_data_dir',
)


def prompt(msg, default=None, type_cast=None):
    """Запрашивает данные от пользователя и возвращает ввод."""
    while True:
        value = input(f'{msg}: ')

        if not value:
            return default

        if type_cast is None:
            return value

        try:
            return type_cast(value)
        except ValueError as err:
            print(err)


def input_int(msg='Введи число', default=None):
    return prompt(msg, default, type_cast=int)


def input_float(msg='Введите число', default=None):
    return prompt(msg, default, type_cast=float)


def input_datetime(msg='Введите дату', default=None,
                   ftm='%Y-%m-%d %H:%M:%S'):
    return prompt(
        msg,
        default,
        lambda v: datetime.strptime(v, ftm)
    )


def input_date(msg='Введите дату', default=None, ftm='%Y-%m-%d'):
    value = input_datetime(msg, default, ftm)

    if value is None:
        return default

    return value.date() if isinstance(value, datetime) else value


def print_table(headers, iterable):
    """
    Распечатывает таблицу на экран.

    Arguments:
        headers (tuple|list): заголовки колонок таблицы.
        iterable (iterable): строки (данные) таблицы.
    """
    table = PrettyTable(headers)

    for row in iterable:
        table.add_row(row)

    print(table)


def make_dirs_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, 0o755)  # mkdir -p
    return path


user_config_dir = make_dirs_if_not_exists(appdirs.user_config_dir(__package__))
user_data_dir = make_dirs_if_not_exists(appdirs.user_data_dir(__package__))


if __name__ == '__main__':

    dt = input_datetime(default=datetime.now())
    print(dt, type(dt))
