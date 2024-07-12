
from restaurantmanager import db
from restaurantmanager.models import User
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[(
        '1', 'Metamask'), ('2', 'Google'), ('3', 'Email')])
    web3_address = StringField('Web3 Address', validators=[
                               InputRequired(), Length(42)])
    google_id = StringField('Google ID')
    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(
        min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo(
        'password', message='Passwords must match')], render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Register')

    def validate_username(self, username):
        web3_address = db.session.query(User).filter_by(
            web3_address=web3_address.data).first()
        if web3_address:
            raise ValidationError('The web3 address is already in use')


class LoginForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[(
        1, 'Metamask'), (2, 'Google'), (3, 'Email')])
    web3_address = StringField('Web3 Address', validators=[
                               InputRequired(), Length(42)])
    google_id = StringField('Google ID')
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Login')
