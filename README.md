## Setup

### Running

#### Run Local

```
python3 -m venv venv
source venv/bin/activate
sh setup.sh
sh run.sh
```

## Vulns

### Hardcoded Credentials and Keys

```py
# db_helper.py
self.host = '10.0.0.99'
self.port = 3306
self.user = 'MyDbUser'
self.password = 'M1DbPassword'
```

```py
# api_keys.py

GOOGLE_RECAPTCHA_SITE_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
GOOGLE_RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
```

```html
<!-- base.html -->
 <script>
    // var googleCaptchaKey = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI';
    // var googleCatpchaSecretKey = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe';

    var googleCaptchaKey = '{{ GOOGLE_RECAPTCHA_SITE_KEY }}';
    var googleCatpchaSecretKey = '{{ GOOGLE_RECAPTCHA_SECRET_KEY }}';

</script>
```


### SQL Injection

URL: http://localhost:5000/sql-injection/login

```py
# vulns/sql_injection/sql_injection_login.py

username = form.get('username')
password = form.get('password')
password_hash = _hash_password(password)

sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password_hash}'"

db_result = app.db_helper.execute_read(sql)
```

URL: http://localhost:5000/sql-injection/search

```py
# vulns/sql_injection/sql_injection_search.py

search = request.args.get('q')

sql = f"SELECT * FROM products WHERE name LIKE '%{search}%'"

db_result = app.db_helper.execute_read(sql)
```

### XSS

Reflected: http://localhost:5000/xss/reflected?search=

```html
<!--
    Reflected
    templates/xss-reflected.html line 11
-->

{{ request.args.get('search') }}
```

Stored: http://localhost:5000/xss/stored

```html
<!--
    Stored
    templates/xss-stored.html line 33
-->

{% for msg in messages %}
    <li>
        <td>{{ msg }}</td>
    </li>
{% endfor %}
```

### IFrame Injection

URL: http://localhost:5000/iframe-injection?page=/static/pages/about.html

```py
# The attacker could set the page arg to an evil url and share it with the victim.
# Just change the URL to: http://localhost:5000/iframe-injection?page=http://example.com

# vulns/iframe_injection/iframe_injection.py
def iframe_injection_page(request, app):
    iframe_url = request.args.get('page')
    return render_template("iframe_injection.html", iframe_url=iframe_url)
```

```html
{% extends "base.html" %}
{% block content %}
<h2>Iframe Injection</h2>

<iframe src="{{ iframe_url }}" frameborder="0"></iframe>

{% endblock %}
```