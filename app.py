import os
# from db_helper import db_helper
from flask import Flask, render_template, request #, redirect, url_for
from vulns.sql_injection.sql_injection_login import sql_injection_login_page, sql_injection_login_api
from vulns.sql_injection.sql_injection_search import sql_injection_search_page
from vulns.xss_injection.xss_reflected import xss_reflected_page
from vulns.iframe_injection.iframe_injection import iframe_injection_page
from vulns.roles.roles_page import roles_page
from middlewares import require_api_key


app = Flask(__name__)


@app.before_request
@require_api_key
def before_request():
    pass


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/role-access-model', methods=['POST'])
def reset_database():

    return roles_page(request, app)


@app.route('/sql-injection/login', methods=['GET', 'POST'])
def sql_injection_login():
    if request.method == 'GET':
        return sql_injection_login_page(request, app)

    return sql_injection_login_api(request, app)


@app.route('/sql-injection/search', methods=['GET'])
def sql_injection_search():
    return sql_injection_search_page(request, app)
    

@app.route('/xss/reflected', methods=['GET'])
def xss_reflected():
    return xss_reflected_page(request, app)


@app.route('/iframe-injection', methods=['GET'])
def iframe_injection():
    return iframe_injection_page(request, app)