from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image_file = db.Column(db.String(64), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False, nullable=False)
    trip = db.relationship('Izlet', backref='kreator', lazy=True)
   
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Izlet(db.Model):
    id_izlet = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    naziv = db.Column(db.String(128), nullable=False)
    destinacija = db.Column(db.String(64), nullable=False)
    cijena = db.Column(db.String(64), nullable=False)
    polazak = db.Column(db.String(64), nullable=False)
    dolazak = db.Column(db.String(64), nullable=False)
    image_file = db.Column(db.String(64), nullable=False, default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    opis = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Izlet {}>'.format(self.opis)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))