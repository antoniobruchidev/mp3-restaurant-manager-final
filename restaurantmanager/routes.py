import os
from flask import redirect, render_template, url_for
from restaurantmanager import app, db, argon2
from restaurantmanager.models import AccountType, Message, User, Wallet, Supplier, BoughtItem, ManufactoredItem, Recipe, SellableItem, StockMovement, Order, Delivery
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from restaurantmanager.forms import LoginForm, RegisterForm


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    g_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    form = LoginForm()
    if form.validate_on_submit():

        if form.account_type.data == '3':
            user = db.session.query(User).filter_by(google_id=form.google_id.data).first()
            if user:
                logged_in = User.query.filter_by(google_id=form.google_id.data).first()
                login_user(logged_in)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'), code=404)
        elif form.account_type.data == '2':
            user = db.session.query(User).filter_by(email=form.email.data).first()
            if user:
                print(user.password)
                if argon2.check_password_hash(user.password, form.password.data):
                   logged_in = User.query.filter_by(email=form.email.data).first()
                login_user(logged_in)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'), code=404)
        elif form.account_type.data == '1':
            user = db.session.query(User).filter_by(web3_address=form.web3_address.data)
            if user:
                logged_in = User.query.filter_by(web3_address=form.web3_address.data).first()
                login_user(logged_in)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'), code=404).first()
            
    return render_template('login.html', form=form, g_client_id=g_client_id)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


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
            hashed_password =argon2.generate_password_hash(form.password.data)
            print(form.password.data, hashed_password)
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
