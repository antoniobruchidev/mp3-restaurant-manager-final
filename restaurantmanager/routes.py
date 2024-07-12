import os
from flask import redirect, render_template, url_for
from restaurantmanager import app, db, bcrypt
from restaurantmanager.models import AccountType, Message, User, Wallet, Supplier, BoughtItem, ManufactoredItem, Recipe, SellableItem, StockMovement, Order, Delivery
from flask_login import UserMixin
from restaurantmanager.forms import LoginForm, RegisterForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    g_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    form = LoginForm()
    return render_template('login.html', form=form, g_client_id=g_client_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    g_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    form = RegisterForm()

    if form.validate_on_submit():
        if form.account_type.data == '3':
            new_user = User(web3_address=form.web3_address.data, account_type=AccountType(
                int(form.account_type.data)), google_id=form.google_id.data)
            db.session.add(new_user)
            db.session.commit()
            user = db.session.query(User).filter_by(
                web3_address=form.web3_address.data).first()
            new_wallet = Wallet(
                user_id=user.id, mnemonic=form.mnemonic.data, priv=form.priv.data)
            db.session.add(new_wallet)
            db.session.commit()
            return redirect(url_for('login'))
        elif form.account_type.data == '2':
            hashed_password =bcrypt.generate_password_hash(form.password.data)
            new_user = User(web3_address=form.web3_address.data, account_type=AccountType(
                int(form.account_type.data)), email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            user = db.session.query(User).filter_by(
                web3_address=form.web3_address.data).first()
            new_wallet = Wallet(
                user_id=user.id, mnemonic=form.mnemonic.data, priv=form.priv.data)
            db.session.add(new_wallet)
            db.session.commit()
            return redirect(url_for('login'))
        elif form.account_type.data == '1':
            new_user = User(web3_address=form.web3_address.data, account_type=AccountType(int(form.account_type.data)))
            db.session.add(new_user)
            db.session.commit()
            user = db.session.query(User).filter_by(
                web3_address=form.web3_address.data).first()
            new_wallet = Wallet(user_id=user.id, mnemonic="EOA", priv="EOA")
            db.session.add(new_wallet)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            print("some problem account type should not be different from given options")
    print(form.errors)

    return render_template('register.html', form=form, g_client_id=g_client_id)
