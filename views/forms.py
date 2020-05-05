from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DecimalField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import Users


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AdsForm(FlaskForm):
    transactionType = SelectField('transactionType', choices=[('1', 'For sale'), ('2', 'For rent')],
                           validators=[DataRequired()])
    roomsNum = IntegerField('roomsNum',
                           validators=[DataRequired()])
    area = IntegerField('area',
                           validators=[DataRequired()])
    price = DecimalField('price',
                        validators=[DataRequired()])
    governorate = StringField('governorate',
                        validators=[DataRequired()])
    location = StringField('location',
                        validators=[DataRequired()])
    mobile = IntegerField('mobile',
                       validators=[DataRequired(), Length(8)])

    description = TextField('description')
    
    submit = SubmitField('Sign Up')
class Form(FlaskForm):
    region = SelectField('region',choices=[('1', 'Select a region')],  validators=[DataRequired()])
    municipality = SelectField('municipality', choices=[('1', 'Select a municipality')], validators=[DataRequired()])
    emplacement = SelectField('emplacement', choices=[('1', 'Select an emplacement')], validators=[DataRequired()])
    area = IntegerField('area',
                        validators=[DataRequired()])
    roomNumber = SelectField('roomNumber', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')],
                           validators=[DataRequired()])
