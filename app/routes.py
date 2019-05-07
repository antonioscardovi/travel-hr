from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app.forms import RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Travel.hr - Homepage')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/homepage')
def homepage():
    return 'Homepage'