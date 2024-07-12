
from restaurantmanager import db
from restaurantmanager.models import User
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[('0', 'Choose your connection option'), (
        '1', 'Metamask'), ('2', 'Email'), ('3', 'Google')])
    web3_address = StringField('Web3 Address', validators=[
                               InputRequired(), Length(42)])
    google_id = StringField('Google ID')
    email = StringField('Email')
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    mnemonic = StringField('Mnemonic', validators=[InputRequired()])
    priv = StringField('Private Key', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_username(self, web3_address):
        existing_web3_address = db.session.query(User).filter_by(
            web3_address=web3_address).first()
        if existing_web3_address:
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
