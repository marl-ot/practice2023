
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()


HOST_DB = os.getenv('HOST_DB')
PORT_DB = os.getenv('PORT_DB')
USER_DB = os.getenv('USER_DB')
NAME_DB = os.getenv('NAME_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')


def connection():
    try:
        connection = psycopg2.connect(
            host=HOST_DB,
            port=PORT_DB,
            user=USER_DB,
            password=PASSWORD_DB,
            database=NAME_DB
        )
        print('[INFO] Успешное подключение к базе данных', e)

    except Exception as e:
        print('[INFO] Ошибка в процессе подключения к базе данных', e)
    return connection


# # Функция для выполнения SQL-запросов
# def execute_query(query):
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute(query)
#     cursor.close()
#     conn.close()


def create_database(name):
    db_params = {
        "host": HOST_DB,
        "user": USER_DB,
        "password": PASSWORD_DB
    }

    create_database_query = f"CREATE DATABASE {name};"
    conn = psycopg2.connect(**db_params)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(create_database_query)
    cursor.close()
    conn.close()

    # Параметры для подключения к новой базе данных banks_test
    db_params["database"] = name

    print(f"[INFO] База данных {name} успешно создана")


def create_tables():
    conn = connection()

    # SQL-запросы для создания таблиц
    queries = [
        """
        CREATE TABLE IF NOT EXISTS person_roles (
            person_role_id SERIAL PRIMARY KEY,
            person_role_name CHAR(32)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS card_types (
            card_type_id SERIAL PRIMARY KEY,
            card_type_name CHAR(32)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS card_statuses (
            card_status_id SERIAL PRIMARY KEY,
            card_status_name CHAR(64)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS payment_account_types (
            payment_account_type_id SERIAL PRIMARY KEY,
            payment_account_type_name CHAR(64)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS international_passports (
            international_passport_id SERIAL PRIMARY KEY,
            lastname CHAR(32),
            firstname CHAR(32),
            surname CHAR(32),
            international_passport_series CHAR(2),
            international_passport_number CHAR(7),
            international_passport_issue_date DATE,
            international_passport_end_date DATE,
            international_passport_whom_issue CHAR(64),
            birth_date DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS visas (
            visa_id SERIAL PRIMARY KEY,
            international_passport_id INTEGER,
            country CHAR(32),
            issue_date DATE,
            end_date DATE,
            FOREIGN KEY (international_passport_id) REFERENCES international_passports(international_passport_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS passports (
            passport_id SERIAL PRIMARY KEY,
            lastname CHAR(32),
            firstname CHAR(32),
            surname CHAR(32),
            passport_series CHAR(4),
            passport_number CHAR(6),
            issue_date DATE,
            whom_issue CHAR(64),
            birth_date DATE,
            registration DATE,
            is_married_mark BOOLEAN,
            international_passport_id INTEGER,
            FOREIGN KEY (international_passport_id) REFERENCES international_passports(international_passport_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS persons (
            person_id SERIAL PRIMARY KEY,
            login CHAR(32),
            password_hash CHAR(64),
            passport_id INTEGER,
            INN BIGINT,
            phone_number CHAR(16),
            SNILS CHAR(16),
            email CHAR(32),
            person_role_id INTEGER,
            secret_word_hash CHAR(64),
            FOREIGN KEY (passport_id) REFERENCES passports(passport_id),
            FOREIGN KEY (person_role_id) REFERENCES person_roles(person_role_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS worker_confirms (
            worker_confirm_id SERIAL PRIMARY KEY,
            person_id INTEGER,
            is_worker_confirm BOOLEAN,
            FOREIGN KEY (person_id) REFERENCES persons(person_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS payment_accounts (
            payment_account_id SERIAL PRIMARY KEY,
            payment_account_number BIGINT,
            balance FLOAT,
            payment_account_type_id INTEGER,
            FOREIGN KEY (payment_account_type_id) REFERENCES payment_account_types(payment_account_type_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id SERIAL PRIMARY KEY,
            transaction_from INTEGER,
            transaction_to INTEGER,
            worker_confirm_id INTEGER,
            amount FLOAT,
            FOREIGN KEY (transaction_from) REFERENCES payment_accounts(payment_account_id),
            FOREIGN KEY (transaction_to) REFERENCES payment_accounts(payment_account_id),
            FOREIGN KEY (worker_confirm_id) REFERENCES worker_confirms(worker_confirm_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS cards (
            card_id SERIAL PRIMARY KEY,
            card_number BIGINT,
            end_date DATE,
            CVV_hash CHAR(64),
            card_status_id INTEGER,
            card_type_id INTEGER,
            person_id INTEGER,
            payment_account_id INTEGER,
            is_active BOOLEAN,
            FOREIGN KEY (payment_account_id) REFERENCES payment_accounts(payment_account_id),
            FOREIGN KEY (person_id) REFERENCES persons(person_id),
            FOREIGN KEY (card_status_id) REFERENCES card_statuses(card_status_id),
            FOREIGN KEY (card_type_id) REFERENCES card_types(card_type_id)
        )
        """
    ]

    # Создание таблиц
    with conn.cursor() as cursor:
        for query in queries:
            cursor.execute(query)
            conn.commit()

    print("[INFO] Таблицы успешно созданы")
    conn.close()


def data_to_tables():
    conn = connection()
    # Данные для заполнения таблицы person_roles:
    person_roles_data = [
        (1, 'Оператор'),
        (2, 'Менеджер'),
        (3, 'Клиент')
    ]
    # SQL-запрос для заполнения таблицы person_roles
    insert_person_roles_query = "INSERT INTO person_roles (person_role_id, person_role_name) VALUES (%s, %s)"


    # Данные для заполнения таблицы card_types:
    card_types_data = [
        (1, 'Дебетовая'),
        (2, 'Кредитная'),
    ]
    # SQL-запрос для заполнения таблицы card_types
    insert_card_types_query = "INSERT INTO card_types (card_type_id, card_type_name) VALUES (%s, %s)"


    # Данные для заполнения таблицы card_statuses:
    card_statuses_data = [
        (1, 'Активна'),
        (2, 'Заблокирована'),
        (3, 'Заморожена'),
    ]
    # SQL-запрос для заполнения таблицы card_statuses
    insert_card_statuses_query = "INSERT INTO card_statuses (card_status_id, card_status_name) VALUES (%s, %s)"


    # Данные для заполнения таблицы payment_account_types:
    payment_account_types_data = [
        (1, 'Основной'),
        (2, 'Депозитный'),
        (3, 'Карточный'),
        (4, 'Бюджетный'),
        (5, 'Лицевой'),
    ]
    # SQL-запрос для заполнения таблицы payment_account_types
    insert_payment_account_types_query = "INSERT INTO payment_account_types (payment_account_type_id, payment_account_type_name) VALUES (%s, %s)"


    # Данные для заполнения таблицы international_passports
    international_passports_data = [
        (5001, 'Иванов', 'Неиван', 'Иванович', 'AA', '1234567', '2020-01-01', '2025-01-01', 'МВД РОССИИ', '2000-01-01'),
        (5002, 'Петр', 'Непетр', 'Петров', 'BB', '7654321', '2021-02-02', '2026-02-02', 'МВД РОССИИ', '2001-02-02'),
    ]
    # SQL-запрос для заполнения таблицы international_passports
    insert_international_passports_query = "INSERT INTO international_passports (international_passport_id, lastname, firstname, surname, international_passport_series, international_passport_number, international_passport_issue_date, international_passport_end_date, international_passport_whom_issue, birth_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


    # Данные для заполнения таблицы visas
    visas_data = [
        (6001, 5001, 'ОАЭ', '2022-01-01', '2022-03-01'),
        (6002, 5002, 'США', '2022-02-02', '2022-04-02'),
    ]
    # SQL-запрос для заполнения таблицы visas
    insert_visas_query = "INSERT INTO visas (visa_id, international_passport_id, country, issue_date, end_date) VALUES (%s, %s, %s, %s, %s)"


    # Данные для заполнения таблицы passports
    passports_data = [
        (1001, 'Иванов', 'Неиван', 'Иванович', '4501', '123456', '2020-01-01', 'МВД РОССИИ', '2000-01-01', '2020-02-02', True, 5001),
        (1002, 'Петр', 'Непетр', 'Петрович', '4502', '654321', '2021-02-02', 'МВД РОССИИ', '2001-02-02', '2021-03-03', False, 5002),
    ]
    # SQL-запрос для заполнения таблицы passports
    insert_passports_query = "INSERT INTO passports (passport_id, lastname, firstname, surname, passport_series, passport_number, issue_date, whom_issue, birth_date, registration, is_married_mark, international_passport_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


    # Данные для заполнения таблицы persons
    persons_data = [
        (101, 'login_1', 'password_hash_1', 1001, 1234567890, '123-456-783 90', '+7 111-11-11 11', 'ivan_1@example.com', 1, 'secret_word_hash_1'),
        (102, 'login_2', 'password_hash_2', 1002, 9876543210, '987-654-323 10', '+7 222-22-22 22', 'petr_1@example.com', 2, 'secret_word_hash_2'),
    ]
    # SQL-запрос для заполнения таблицы persons
    insert_persons_query = "INSERT INTO persons (person_id, login, password_hash, passport_id, INN, phone_number, SNILS, email, person_role_id, secret_word_hash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


    # Данные для заполнения таблицы worker_confirms
    worker_confirms_data = [
        (1, 101, True),
        (2, 102, False),
    ]
    # SQL-запрос для заполнения таблицы worker_confirms
    insert_worker_confirms_query = "INSERT INTO worker_confirms (worker_confirm_id, person_id, is_worker_confirm) VALUES (%s, %s, %s)"


    # Пример для заполнения таблицы payment_accounts
    payment_accounts_data = [
        (1, 1234567890, 1000.50, 1),
        (2, 9876543210, 500.25, 2),
    ]
    # SQL-запрос для заполнения таблицы payment_accounts
    insert_payment_accounts_query = "INSERT INTO payment_accounts (payment_account_id, payment_account_number, balance, payment_account_type_id) VALUES (%s, %s, %s, %s)"


    # Данные для заполнения таблицы transactions
    transactions_data = [
        (1, 1, 2, 1, 100.00),
        (2, 2, 1, 2, 50.25),
    ]
    # SQL-запрос для заполнения таблицы transactions
    insert_transactions_query = "INSERT INTO transactions (transaction_id, transaction_from, transaction_to, worker_confirm_id, amount) VALUES (%s, %s, %s, %s, %s)"


    # Данные для заполнения таблицы cards
    cards_data = [
        (1, 1111111111111111, '2025-12-31', 'cvv_hash_1', 1, 1, 101, 1, True),
        (2, 2222222222222222, '2024-11-30', 'cvv_hash_2', 2, 2, 102, 2, False),
    ]
    # SQL-запрос для заполнения таблицы cards
    insert_cards_query = "INSERT INTO cards (card_id, card_number, end_date, CVV_hash, card_status_id, card_type_id, person_id, payment_account_id, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"


    # Добавление данных
    with conn.cursor() as cursor:
        cursor.executemany(insert_person_roles_query, person_roles_data)
        cursor.executemany(insert_card_types_query, card_types_data)
        cursor.executemany(insert_card_statuses_query, card_statuses_data)
        cursor.executemany(insert_payment_account_types_query, payment_account_types_data)
        cursor.executemany(insert_international_passports_query, international_passports_data)
        cursor.executemany(insert_visas_query, visas_data)
        cursor.executemany(insert_passports_query, passports_data)
        cursor.executemany(insert_persons_query, persons_data)
        cursor.executemany(insert_worker_confirms_query, worker_confirms_data)
        cursor.executemany(insert_payment_accounts_query, payment_accounts_data)
        cursor.executemany(insert_transactions_query, transactions_data)
        cursor.executemany(insert_cards_query, cards_data)
        conn.commit()
    

    print("[INFO] Данные в таблицы успешно добавлены")
    conn.close()


# create_database(NAME_DB)
# create_tables()
# data_to_tables()