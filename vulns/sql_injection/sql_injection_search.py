from flask import render_template
from database import execute_read


def sql_injection_search_page(request):
    search = request.args.get('q')

    sql = f"SELECT * FROM persons WHERE TRIM(login) LIKE '%{search}%'"
    # SELECT * FROM persons WHERE TRIM(login) LIKE '%{'; DROP TABLE persons WITH FORCE; --'}%'"

    db_result = execute_read(sql)

    persons = list(
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
    )

    return render_template(
        'sql_injection/search.html',
        sql=sql,
        persons=persons
    )
