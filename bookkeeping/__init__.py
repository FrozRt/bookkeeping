from collections import OrderedDict, namedtuple
from datetime import datetime, timedelta, date
import pkg_resources
from textwrap import dedent
import sys

from . import helpers as h
from . import storage
from .services import make_connection


Action = namedtuple('Action', ('func', 'title'))
actions = OrderedDict()


def action(cmd, title):
    def decorator(func):
        actions[str(cmd)] = Action(func, title)
        return func
    return decorator


def input_payment_name():
    """Запрашивает идентификатор платежа и возвращает его из БД."""
    payment_name_id = h.input_int('Введите ID платежа')
    payment = storage.get_payment(payment_name_id)

    if payment is None:
        print(f'Платеж с ID {payment_name_id} не найден.')

    return payment


def input_payment_name_data(payment=None):
    """Ввод данных о платеже"""
    payment = dict(payment) if payment is not None else {}
    data = {}

    data['payment_name'] = h.prompt(
        'Наименования платежа', default=payment.get('payment_name')
    )

    data['price'] = h.prompt(
        'Стоимость', default=payment.get('price', '')
    )

    data['amount'] = h.prompt(
        'Количество', default=payment.get('amount', '')
    )

    return data


@action(1, 'Добавить платеж')
def add_payment_name():
    data = input_payment_name_data()
    storage.create_payment(**data)
    print(f'Платеж "{data["payment_name"]}" успешно сохранен.')


@action(2, 'Отредактировать платеж')
def edit_payment_name():
    edit_p = input_payment_name()

    if edit_p is not None:
        data = input_payment_name_data(edit_p)
        storage.update_payment_name(edit_p['id'], **data)
        print(f'Информация о платеже "{edit_p["payment_name"]}" успешно отредактирована.')


@action(3, 'Вывести все платежи за указанный период')
def print_all_payment_names_for_period():
    created = h.input_date('Введите дату', default=date.today())
    payment_names = storage.get_payments_per_date(created)
    h.print_table(['ID', 'Наименования платежа', 'Стоимость', 'Количество', 'Создано'], payment_names)


@action(4, 'Вывести топ самых крупных платежей')
def print_top_biggest_payment_names():
    payments = storage.get_top_biggest_payments()
    h.print_table(['ID', 'Наименования платежа', 'Создано'], payments)


@action(5, 'Вывести все платежи')
def print_all_payments():
    payment_names = storage.get_all_payments()
    h.print_table(['ID', 'Наименования платежа', 'Стоимость', 'Количество', 'Создано'], payment_names)


@action(6, 'Удалить платеж')
def delete():
    payment_name_id = h.input_int('Введите ID платежа')
    payment = storage.delete_payment(payment_name_id)
    print('Платеж успешно удален')
    return payment


@action('m', 'Показать меню')
def action_show_menu():
    for cmd, action in actions.items():
        print(f'{cmd}. {action.title}')


@action('q', 'Выйти')
def action_exit():
    sys.exit(0)


def main():
    scnhema_path = pkg_resources.resource_filename(__package__, 'resources/schema.sql')
    storage.initialize(scnhema_path)

    action_show_menu()

    while True:
        cmd = input('\nВведите команду: ').strip()
        action = actions.get(cmd)

        if action:
            action.func()
        else:
            print('Вы ввели не верную команду')
