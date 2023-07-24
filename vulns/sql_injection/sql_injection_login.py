from flask import render_template
from database import execute_read
import hashlib


def sql_injection_login_page(request, app):
    return render_template(
        'sql_injection/login.html',
        sql='',
        logged=None
    )


def sql_injection_login_api(request, app):
    form = request.form

    username = form.get('username')
    password = form.get('password')
    password_hash = password #_hash_password(password)

    sql = f"SELECT * FROM persons WHERE login='{username}' AND password_hash='{password_hash}'"
    # ' OR 1=1; --
    
    db_result = execute_read(sql)

    user = list(
        map(
            lambda p: {
                'id': p[0],
                'login': p[1],
                'password': p[2],
                'passport_id': p[3],
                'inn': p[4],
                'phone_number': p[5],
                'snils': p[6],
                'email': p[7],
                'person_role_id': p[8],
            },
            db_result
        )
    )[0] if len(db_result) > 0 else None

    return render_template(
        'sql_injection/login.html',
        sql=sql,
        logged=user is not None
    )


# def _hash_password(password):
#     md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
#     return md5_pass