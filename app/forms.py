from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form, TextField, TextAreaField, validators 
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField
from app.models import User
from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class IzletiForm(FlaskForm):
    name = StringField('Ime Izleta', validators=[DataRequired()])
    location = StringField('Destinacija', validators=[DataRequired()])
    start = DateField('Datum Početka Izleta', format='%Y-%m-%d', validators=[DataRequired()])
    end = DateField('Kraj izleta', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Opis Izleta', validators=[DataRequired()])
    price = StringField('Cijena', validators=[DataRequired()])
    picture = FileField('Fotografija', validators=[FileRequired()])
    submit = SubmitField('Submit')
