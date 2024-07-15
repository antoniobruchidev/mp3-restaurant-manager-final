import os
from flask import redirect, render_template, url_for
from restaurantmanager import app, db, argon2, mail
from restaurantmanager.models import AccountType, InternalMessage, User, Wallet, Supplier, BoughtItem, ManufactoredItem, Recipe, SellableItem, StockMovement, Order, Delivery
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from restaurantmanager.forms import LoginForm, RegisterForm
from restaurantmanager.web3interface import w3, check_role, grant_role, role_hash
from flask_mail import Message


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
            user = db.session.query(User).filter_by(
                google_id=form.google_id.data).first()
            
            if user:
                logged_in = User.query.filter_by(
                    google_id=form.google_id.data).first()
                login_user(logged_in)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
        elif form.account_type.data == '2':
            user = db.session.query(User).filter_by(
                email=form.email.data).first()
            if user:
                if user.activated:
                    if argon2.check_password_hash(user.password, form.password.data):
                        logged_in = User.query.filter_by(
                            email=form.email.data).first()
                    login_user(logged_in)
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))
        elif form.account_type.data == '1':
            user = db.session.query(User).filter_by(
                web3_address=form.web3_address.data).first()
            if user:
                logged_in = User.query.filter_by(
                    web3_address=form.web3_address.data).first()
                login_user(logged_in)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))

    return render_template('login.html', form=form, g_client_id=g_client_id)


@app.route('/dashboard')
@login_required
def dashboard():
    is_owner = check_role(role_hash('owner'), current_user.web3_address)
    is_manager = check_role(role_hash('manager'), current_user.web3_address)
    is_chef = check_role(role_hash('chef'), current_user.web3_address)
    is_waiter = check_role(role_hash('waiter'), current_user.web3_address)
    web3_address = current_user.web3_address
    if current_user.f_name != 'EOA':
        f_name = current_user.f_name
    else:
        f_name = ""
    if current_user.l_name != 'EOA':
        l_name = current_user.l_name
    else:
        l_name = ""
    email = current_user.email

    return render_template('dashboard.html', is_owner=is_owner, is_manager=is_manager, is_chef=is_chef, is_waiter=is_waiter, web3_address=web3_address, f_name=f_name, l_name=l_name, email=email)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    g_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    form = RegisterForm()

    if form.validate_on_submit():
            hashed_password = argon2.generate_password_hash(form.password.data)
            activated = False
            if form.account_type.data != '2':
                activated = True
            new_user = User(f_name=form.f_name.data, l_name=form.l_name.data, password=hashed_password, email=form.email.data, google_id=form.google_id.data, web3_address=form.web3_address.data, account_type=AccountType(
                int(form.account_type.data)), activated=activated)
            db.session.add(new_user)
            db.session.commit()
            user = db.session.query(User).filter_by(web3_address=form.web3_address.data).first()
            msg = Message("Please activate your account",
                          sender=os.environ.get('MAIL_USERNAME'),
                          recipients=[form.email.data])
            msg.body = f"Hello {user.f_name}, \n\nPlease click on the link below to activate your account.\n\nhttp://localhost:50082/activate/{form.web3_address.data}\n\nThanks."
            mail.send(msg)
            new_wallet = Wallet(user_id=user.id, mnemonic=form.mnemonic.data, priv=form.priv.data)
            db.session.add(new_wallet)
            db.session.commit()
            return redirect(url_for('login'))
    print(form.errors)

    return render_template('register.html', form=form, g_client_id=g_client_id)

@app.route('/activate/<web3_address>')
def activate(web3_address):
    print(web3_address)
    user = db.session.query(User).filter_by(web3_address=web3_address).first()
    print(user.activated)
    if user.activated:
        return redirect(url_for('login'))
    else:
        user.activated = True
        db.session.commit()
        return redirect(url_for('login'))