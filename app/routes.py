from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegistrationForm, IzletiForm, EditProfileForm
from app.models import User, Izlet
import os

@app.route('/')
@app.route('/index')
def index():
    izleti = Izlet.query.all()
    izlet1 = Izlet.query.filter_by(id_izlet=1).first()
    izlet2 = Izlet.query.filter_by(id_izlet=2).first()
    izlet3 = Izlet.query.filter_by(id_izlet=3).first()
    slika1 = izlet1.image_file
    return render_template('index.html', title='Travel.hr - Homepage', izleti=izleti, izlet1=izlet1, izlet2=izlet2, izlet3=izlet3, slika1=slika1)

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
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    if form.validate_on_submit():
        f = request.files['picture']
        filename=secure_filename(f.filename)
        izlet = Izlet(naziv=form.name.data, destinacija=form.location.data, cijena=form.price.data, 
        dolazak=form.end.data, polazak=form.start.data, opis=form.description.data, user_id=current_user.id, image_file=f.filename)
        db.session.add(izlet)
        db.session.commit()
                
        f.save(os.path.join(app.config['TRIP_UPLOAD_FOLDER'], filename))
        
        flash('Congratulations, you posted a trip!')
        return redirect(url_for('homepage'))
    return render_template('izleti.html', title='Add Trips', form=form)


@app.route('/homepage')
@login_required
def homepage():
    izlet1 = Izlet.query.filter_by(id_izlet=1).first()
    izlet2 = Izlet.query.filter_by(id_izlet=2).first()
    izlet3 = Izlet.query.filter_by(id_izlet=3).first()
    return render_template('homepage.html', title='Homepage', izlet1=izlet1, izlet2=izlet2, izlet3=izlet3)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm()
    return render_template('profile.html', form=form, user=user)


@app.route('/trips')
@login_required
def trips():
    izlet = Izlet.query.all()
    return render_template('trips.html', izlet=izlet)

@app.route('/detalji/<tripid>')
@login_required
def detalji(tripid):
    izlet = Izlet.query.filter_by(id_izlet=tripid).first_or_404()
    return render_template('detalji.html', izlet=izlet)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    picture = request.files['Fotografija']
    return picture.filename

# @app.route('/profilUser')
# @login_required
# def profilUser(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('profileUser.html', user=user)