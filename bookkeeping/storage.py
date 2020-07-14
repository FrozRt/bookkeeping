from datetime import datetime, time
from .decorators import with_connection


SQL_CREATE_NEW_PAYMENT_NAME = 'INSERT INTO bookkeeping (payment_name, price, amount) VALUES (?, ?, ?)'

SQL_SELECT_ALL_PAYMENTS = '''
    SELECT
        id, payment_name, price, amount, created
    FROM
        bookkeeping
'''

SQL_UPDATE_PAYMENT_NAME = '''
    UPDATE bookkeeping SET
        payment_name=?, price=?, amount=?
    WHERE id=?
'''

SQL_SELECT_TOP_BIGGEST_PAYMENTS = '''
    SELECT
        id, payment_name, created
    FROM
        bookkeeping
    ORDER BY price*amount DESC LIMIT 3
'''

SQL_DELETE = '''
    DELETE FROM bookkeeping WHERE id=?
'''
SQL_SELECT_PAYMENT_BY_PK = f'{SQL_SELECT_ALL_PAYMENTS} WHERE id=?'

SQL_SELECT_PAYMENTS_PER_DATE = f'{SQL_SELECT_ALL_PAYMENTS} WHERE created BETWEEN ? AND ?'


@with_connection()
def initialize(conn, creation_schema):
    """Используя переданный скрипт, инициализирует структуру БД."""
    with open(creation_schema) as f:
        conn.executescript(f.read())


@with_connection()
def create_payment(conn, payment_name, price, amount=1):
    """Сохраняет новую задачу в БД и возвращает ее."""
    conn.execute(
        SQL_CREATE_NEW_PAYMENT_NAME,
        (payment_name, price, amount)
    )


@with_connection()
def update_payment_name(conn, pk, payment_name, price, amount=1):
    """Обновляет задачу в БД."""
    conn.execute(
        SQL_UPDATE_PAYMENT_NAME,
        (payment_name, price, amount, pk)
    )


@with_connection()
def get_payment(conn, pk):
    """Выбирает и возвращает из БД платеж с указанным идентификатором, либо исключение типа TaskError."""
    cursor = conn.execute(SQL_SELECT_PAYMENT_BY_PK, (pk,))
    return cursor.fetchone()


@with_connection()
def get_payments_per_date(conn, dt):
    """Возвращает платежи за указанную дату."""
    dt_end = datetime.combine(dt, time(23, 59, 59))
    cursor = conn.execute(
        SQL_SELECT_PAYMENTS_PER_DATE, (dt, dt_end)
    )
    return cursor.fetchall()


@with_connection()
def delete_payment(conn, pk):
    cursor = conn.execute(SQL_DELETE, (pk,))
    return cursor.fetchone()


@with_connection()
def get_all_payments(conn):
    """Возвращает все платежи из БД."""
    return conn.execute(SQL_SELECT_ALL_PAYMENTS).fetchall()


@with_connection()
def get_top_biggest_payments(conn):
    return conn.execute(SQL_SELECT_TOP_BIGGEST_PAYMENTS)
