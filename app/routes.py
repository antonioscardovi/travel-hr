from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegistrationForm, IzletiForm
from app.models import User, Izlet

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Travel.hr - Homepage')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, name=form.name.data, surname=form.surname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/izleti', methods=['GET', 'POST'])
@login_required
def izleti():
    form = IzletiForm()
    if current_user.is_authenticated:
        return render_template('izleti.html', title="Izleti", form=form)
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    if form.validate_on_submit():
        izlet = Izlet(naziv=form.name.data, destinacija=form.location.data, cijena=form.price.data, 
        dolazak=form.end.data, polazak=form.start.data, image_file=form.picture.data, 
        date_posted=form.datum.data, opis=form.description.data)
        db.session.add(izlet)
        db.session.commit()
        flash('Congratulations, you posted a trip!')
        print('Congratulations!')
        return redirect(url_for('homepage'))
    return render_template('homepage.html', title='Homepage')


@app.route('/homepage')
@login_required
def homepage():
    return render_template('homepage.html', title='Homepage')


@app.route('/profile/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    return render_template('profile.html', user=user)