from flask import render_template
from database import execute_read


def xss_reflected_page(request, app):
    search = request.args.get('search')

    persons = execute_read(
        f"SELECT * FROM persons WHERE TRIM(login) LIKE '%{search}%'",
        { 'search': f'%{search}%' }
    )

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
            persons
        )
    )

    return render_template(
        'xss_injection/xss-reflected.html',
        persons=persons
    )
