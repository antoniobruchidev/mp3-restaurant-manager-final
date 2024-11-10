
from restaurantmanager import db
from restaurantmanager.models import User, AccountType
from wtforms import IntegerField, StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[(
        '0', 'Choose your connection option'), (
        '1', 'Metamask'), ('2', 'Email'), ('3', 'Google')],
        validators=[InputRequired()])
    web3_address = StringField('Web3 Address', validators=[
                               InputRequired(), Length(42)])
    google_id = StringField('Google ID')
    f_name = StringField('First Name')
    l_name = StringField('Last Name')
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(8, 42)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    mnemonic = StringField('Mnemonic', validators=[InputRequired()])
    priv = StringField('Private Key', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_web3_address(self, web3_address):
        existing_web3_address = db.session.query(User).filter_by(
            web3_address=web3_address.data).first()
        if existing_web3_address:
            raise ValidationError('The web3 address is already in use')
        
    def validate_email(self, email):
        existing_email = db.session.query(User).filter_by(
            email=email.data).first()
        if existing_email:
            raise ValidationError('The email is already in use')
        
    def validate_account_type(self, account_type):
        if account_type.data == '0':
            raise ValidationError('Please choose an account type')


class LoginForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[(
        '0', 'Choose your connection option'),
        ('1', 'Metamask'), ('2', 'Email'), ('3', 'Google')])
    web3_address = StringField('Web3 Address')
    google_id = StringField('Google ID')
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Login')


class CreateMessageForm(FlaskForm):
    subject = StringField('Subject', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    board_id = SelectField('Board', choices=[('0', 'Choose a board'), ('1', 'Owners board'), ('2', 'Managers board'), ('3', 'Chefs board'), ('4', 'Waiters board')])
    submit = SubmitField('Send')

    def validate_board_id(self, board_id):
        if board_id.data == '0':
            raise ValidationError('Please choose a messageboard')
        

class AnswerMessageForm(FlaskForm):
    answer = TextAreaField('Answer', validators=[InputRequired()])
    submit = SubmitField('Send')
    

class AddEmployeeForm(RegisterForm):
    role = SelectField('Role', choices=[('0', 'Choose a role'), ('1', 'Manager'), ('2', 'Chef'), ('3', 'Waiter')])
    submit = SubmitField('Add Employee')
    def validate_role(self, role):
        if role.data == 0:
            raise ValidationError('Please choose a role')
        

class AddSupplierForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone = StringField('Phone Number')
    info = TextAreaField('Info', validators=[InputRequired()])
    submit = SubmitField('Add Supplier')


class AddIngredientForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    supplier_id = IntegerField('Supplier ID', validators=[InputRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Item')

    def validate_supplier_id(self, supplier_id):
        if supplier_id.data == 0:
            raise ValidationError('Please choose a supplier')

