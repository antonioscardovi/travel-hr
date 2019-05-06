from flask import render_template
from flask_login import current_user, login_user, logout_user, login_required
from app import app

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Travel.hr - Homepage')

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
