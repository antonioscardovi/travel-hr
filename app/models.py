from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image_file = db.Column(db.String(64), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False, nullable=False)
    trip = db.relationship('Izlet', backref='kreator', lazy=True)
   
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


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

