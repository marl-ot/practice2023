from flask import render_template
from database import execute_read
import time


def roles_page(request):

    payment_account_types = execute_read(f"SELECT * FROM payment_account_types")
    card_statuses = execute_read(f"SELECT * FROM card_statuses;")
    payment_accounts = execute_read(f"SELECT * FROM payment_accounts;")
    worker_confirms = execute_read(f"SELECT * FROM worker_confirms;")
    transactions = execute_read(f"SELECT * FROM transactions;")
    cards = execute_read(f"SELECT * FROM cards;")
    card_types = execute_read(f"SELECT * FROM card_types;")
    persons = execute_read(f"SELECT * FROM persons;")
    passports = execute_read(f"SELECT * FROM passports;")
    person_roles = execute_read(f"SELECT * FROM person_roles;")
    international_passports = execute_read(f"SELECT * FROM international_passports;")
    visas = execute_read(f"SELECT * FROM visas;")

    payment_account_types = list(
        map(
            lambda p: {
                'payment_account_type_id': p[0],
                'payment_account_type_name': p[1]
            },
            payment_account_types
        )
    )

    card_statuses = list(
        map(
            lambda c: {
                'card_status_id': c[0],
                'card_status_name': c[1]
            },
            card_statuses
        )
    )

    payment_accounts = list(
        map(
            lambda pa: {
                'payment_account_id': pa[0],
                'payment_account_number': pa[1],
                'balance': pa[2],
                'payment_account_type_id': pa[3]
            },
            payment_accounts
        )
    )

    worker_confirms = list(
        map(
            lambda wc: {
                'worker_confirm_id': wc[0],
                'person_id': wc[1],
                'is_worker_confirm': wc[2]
            },
            worker_confirms
        )
    )

    transactions = list(
        map(
            lambda t: {
                'transaction_id': t[0],
                'transaction_from': t[1],
                'transaction_to': t[2],
                'worker_confirm_id': t[3],
                'amount': t[4]
            },
            transactions
        )
    )

    cards = list(
        map(
            lambda card: {
                'card_id': card[0],
                'card_number': card[1],
                'end_date': card[2],
                'CVV_hash': card[3],
                'card_status_id': card[4],
                'card_type_id': card[5],
                'person_id': card[6],
                'payment_account_id': card[7],
                'is_active': card[8]
            },
            cards
        )
    )

    card_types = list(
        map(
            lambda ct: {
                'card_type_id': ct[0],
                'card_type_name': ct[1]
            },
            card_types
        )
    )

    persons = list(
        map(
            lambda person: {
                'person_id': person[0],
                'login': person[1],
                'password_hash': person[2],
                'passport_id': person[3],
                'INN': person[4],
                'phone_number': person[5],
                'SNILS': person[6],
                'email': person[7],
                'person_role_id': person[8],
                'secret_word_hash': person[9]
            },
            persons
        )
    )

    passports = list(
        map(
            lambda pp: {
                'passport_id': pp[0],
                'lastname': pp[1],
                'firstname': pp[2],
                'surname': pp[3],
                'passport_series': pp[4],
                'passport_number': pp[5],
                'issue_date': pp[6],
                'whom_issue': pp[7],
                'birth_date': pp[8],
                'registration': pp[9],
                'is_married_mark': pp[10],
                'international_passport_id': pp[11]
            },
            passports
        )
    )

    person_roles = list(
        map(
            lambda pr: {
                'person_role_id': pr[0],
                'person_role_name': pr[1]
            },
            person_roles
        )
    )

    international_passports = list(
        map(
            lambda ip: {
                'international_passport_id': ip[0],
                'surname': ip[3],
                'firstname': ip[2],
                'lastname': ip[1],
                'international_passport_series': ip[4],
                'international_passport_number': ip[5],
                'international_passport_issue_date': ip[6],
                'international_passport_end_date': ip[7],
                'international_passport_whom_issue': ip[8],
                'birth_date': ip[9]
            },
            international_passports
        )
    )

    visas = list(
        map(
            lambda visa: {
                'visa_id': visa[0],
                'international_passport_id': visa[1],
                'country': visa[2],
                'issue_date': visa[3],
                'end_date': visa[4]
            },
            visas
        )
    )

    # context = {
    #     "payment_account_types": payment_account_types,
    #     # "card_statuses": card_statuses,
    #     # "payment_accounts": payment_accounts,
    #     # "worker_confirms": worker_confirms,
    #     # "transactions": transactions,
    #     # "cards": cards,
    #     # "card_types": card_types,
    #     # "persons": persons,
    #     # "passports": passports,
    #     # "person_roles": person_roles,
    #     # "international_passports": international_passports,
    #     # "visas": visas
    # }

    return render_template(
        'roles/roles_page.html',
        payment_account_types=payment_account_types,
        card_statuses=card_statuses,
        payment_accounts=payment_accounts,
        worker_confirms=worker_confirms,
        transactions=transactions,
        cards=cards,
        card_types=card_types,
        persons=persons,
        passports=passports,
        person_roles=person_roles,
        international_passports=international_passports,
        visas=visas
    )
