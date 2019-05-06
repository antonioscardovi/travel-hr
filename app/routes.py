from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Travel.hr - Homepage')

@app.route('/login')
def login():
    return render_template('login.html')