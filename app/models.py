from app import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), index=True) #Rola admin (2) ili user(1)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.String(64), db.ForeignKey('role.id'))
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

class UserOnIzlet(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    izlet_id = db.Column(db.Integer, db.ForeignKey('izlet.id'))