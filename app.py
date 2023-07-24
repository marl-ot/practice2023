import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_login import current_user
from vulns.sql_injection.sql_injection_login import sql_injection_login_page, sql_injection_login_api
from vulns.sql_injection.sql_injection_search import sql_injection_search_page
from vulns.xss_injection.xss_reflected import xss_reflected_page
from vulns.iframe_injection.iframe_injection import iframe_injection_page
# from werkzeug.security import generate_password_hash, check_password_hash
from vulns.roles.roles_page import roles_page
from middlewares import require_api_key
# from dotenv import load_dotenv
# load_dotenv()


# HOST_DB = os.getenv('HOST_DB')
# PORT_DB = os.getenv('PORT_DB')
# USER_DB = os.getenv('USER_DB')
# NAME_DB = os.getenv('NAME_DB')
# PASSWORD_DB = os.getenv('PASSWORD_DB')


app = Flask(__name__)
# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY


# # Настройка подключения к базе данных PostgreSQL
# conn = psycopg2.connect(
#     host=HOST_DB,
#     port=PORT_DB,
#     user=USER_DB,
#     password=PASSWORD_DB,
#     database=NAME_DB
# )

# def register_user(login, password, phone_number, email):
#     try:
#         cur = conn.cursor()
#         hashed_password = generate_password_hash(password)
#         cur.execute(
#             "INSERT INTO persons (login, password_hash, phone_number, email) VALUES (%s, %s, %s, %s)",
#             (login, hashed_password, phone_number, email)
#         )
#         conn.commit()
#         cur.close()
#         flash('Регистрация прошла успешно. Теперь вы можете войти.', 'Успех')
#         return True
#     except Exception as e:
#         flash('Логин занят, пожалуйста, выберите другой', 'Ошибка')
#         return False


# def login_user(login, password):
#     cur = conn.cursor()
#     cur.execute("SELECT password_hash FROM persons WHERE login = %s", (login,))
#     result = cur.fetchone()
#     cur.close()

#     if result and check_password_hash(result[0], password):
#         flash(f'Добро пожаловать, {login}!', 'Успех')
#         return True
#     else:
#         flash('Ошибка, проверьте логин или пароль', 'Ошибка')
#         return False

@app.route("/")
def home():
    return render_template('home.html')


# # def get_current_user():
# #     return current_user


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         login = request.form['login']
#         password = request.form['password']
#         phone_number = request.form['phone_number']
#         email = request.form['email']
#         if register_user(login, password, phone_number, email):
#             return redirect(url_for('login'))
#     return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         login = request.form['login']
#         password = request.form['password']
#         if login_user(login, password):
#             return redirect(url_for('home'))
#     return render_template('login.html')


# @app.before_request
# @require_api_key
# def before_request():
#     pass


@app.route('/role_access_model', methods=['GET', 'POST'])
def role_access_model():
    return roles_page(request)


@app.route('/sql-injection/login', methods=['GET', 'POST'])
def sql_injection_login():
    if request.method == 'GET':
        return sql_injection_login_page(request)

    return sql_injection_login_api(request)


@app.route('/sql-injection/search', methods=['GET'])
def sql_injection_search():
    return sql_injection_search_page(request)
    

@app.route('/xss/reflected', methods=['GET'])
def xss_reflected():
    return xss_reflected_page(request)


@app.route('/iframe-injection', methods=['GET'])
def iframe_injection():
    return iframe_injection_page(request)