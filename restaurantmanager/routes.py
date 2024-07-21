import os
import datetime
from flask import flash, redirect, render_template, request, url_for
from restaurantmanager import app, db, argon2, mail
from restaurantmanager.models import (
    AccountType,
    Board,
    BoardMessage,
    IngredientQuantity,
    ItemKind,
    ManufactoredIngredientQuantity,
    User,
    Wallet,
    Supplier,
    Ingredient,
    ManufactoredIngredient,
    Recipe,
    StockMovement,
    Order,
    Delivery,
)
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
from restaurantmanager.forms import (
    AddIngredientForm,
    AddEmployeeForm,
    AddSupplierForm,
    CreateMessageForm,
    LoginForm,
    RegisterForm,
)
from restaurantmanager.web3interface import w3, check_role, grant_role, role_hash
from flask_mail import Message


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    g_client_id = os.environ.get("GOOGLE_CLIENT_ID")
    form = LoginForm()
    if form.validate_on_submit():

        if form.account_type.data == "3":
            user = (
                db.session.query(User).filter_by(google_id=form.google_id.data).first()
            )

            if user:
                logged_in = User.query.filter_by(google_id=form.google_id.data).first()
                login_user(logged_in)
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("login"))
        elif form.account_type.data == "2":
            user = db.session.query(User).filter_by(email=form.email.data).first()
            if user:
                if user.activated:
                    if argon2.check_password_hash(user.password, form.password.data):
                        logged_in = User.query.filter_by(email=form.email.data).first()
                    login_user(logged_in)
                    return redirect(url_for("dashboard"))
                else:
                    return redirect(url_for("login"))
            else:
                return redirect(url_for("login"))
        elif form.account_type.data == "1":
            user = (
                db.session.query(User)
                .filter_by(web3_address=form.web3_address.data)
                .first()
            )
            if user:
                logged_in = User.query.filter_by(
                    web3_address=form.web3_address.data
                ).first()
                login_user(logged_in)
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("login"))

    return render_template("login.html", form=form, g_client_id=g_client_id)


@app.route("/dashboard")
@login_required
def dashboard():
    is_owner = check_role(role_hash("owner"), current_user.web3_address)
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    web3_address = current_user.web3_address
    if current_user.f_name != "EOA":
        f_name = current_user.f_name
    else:
        f_name = ""
    if current_user.l_name != "EOA":
        l_name = current_user.l_name
    else:
        l_name = ""
    email = current_user.email
    my_messages = (
        db.session.query(BoardMessage).filter_by(sender_id=current_user.id).all()
    )

    return render_template(
        "dashboard.html",
        is_owner=is_owner,
        is_manager=is_manager,
        is_chef=is_chef,
        is_waiter=is_waiter,
        web3_address=web3_address,
        f_name=f_name,
        l_name=l_name,
        email=email,
        messages=my_messages,
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/messageboard")
@login_required
def messageboard():
    is_owner = check_role(role_hash("owner"), current_user.web3_address)
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_owner:
        owner_messages = (
            db.session.query(BoardMessage).filter_by(board=Board.owner).all()
        )
    else:
        owner_messages = []
    if is_manager:
        manager_messages = (
            db.session.query(BoardMessage).filter_by(board=Board.manager).all()
        )
    else:
        manager_messages = []
    if is_chef:
        chef_messages = (
            db.session.query(BoardMessage).filter_by(board=Board.chef).all()
        )
    else:
        chef_messages = []
    if is_waiter:
        waiter_messages = (
            db.session.query(BoardMessage).filter_by(board=Board.waiter).all()
        )
    else:
        waiter_messages = []
    public_messages = (
        db.session.query(BoardMessage).filter_by(board=Board.public).all()
    )
    board_messages = (
        owner_messages
        + manager_messages
        + chef_messages
        + waiter_messages
        + public_messages
    )

    return render_template("messageboard.html", board_messages=board_messages)


@app.route("/messageboards/sendmessage", methods=["GET", "POST"])
@login_required
def sendmessage():
    date = datetime.datetime.now()
    print(date)
    form = CreateMessageForm()
    if form.validate_on_submit():
        message = BoardMessage(
            sender_id=current_user.id,
            subject=form.subject.data,
            board=Board(int(form.board_id.data)),
            message=form.message.data,
            timestamp=date,
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("sendmessage.html", form=form)


@app.route("/owner/staff")
@login_required
def get_employees():
    is_owner = check_role(role_hash("owner"), current_user.web3_address)
    if is_owner:
        employees = db.session.query(User).filter_by(roles=True).all()
        print(employees)
        return render_template("staff.html", employees=employees)
    else:
        return redirect(url_for("dashboard"))


@app.route("/owner/addemployee", methods=["GET", "POST"])
@login_required
def add_employee():
    is_owner = check_role(role_hash("owner"), current_user.web3_address)
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_owner or is_manager:
        form = AddEmployeeForm()
        if form.validate_on_submit():
            if not is_owner and form.roles.data == "1":
                return redirect(
                    url_for("add_employee"),
                    form=form,
                    g_client_id=os.environ.get("GOOGLE_CLIENT_ID"),
                )
            hashed_password = argon2.generate_password_hash(form.password.data)
            activated = False
            if form.account_type.data != "2":
                activated = True
            new_user = User(
                f_name=form.f_name.data,
                l_name=form.l_name.data,
                password=hashed_password,
                email=form.email.data,
                google_id=form.google_id.data,
                web3_address=form.web3_address.data,
                account_type=AccountType(int(form.account_type.data)),
                activated=activated,
                roles=True,
            )
            db.session.add(new_user)
            db.session.commit()
            user = (
                db.session.query(User)
                .filter_by(web3_address=form.web3_address.data)
                .first()
            )
            msg = Message(
                "Please activate your account",
                sender=os.environ.get("MAIL_USERNAME"),
                recipients=[form.email.data],
            )
            msg.body = f"Hello {user.f_name}, \n\nPlease click on the link below to activate your account.\n\nhttps://carpez-kitchen-manager-e9e93ef660cf.herokuapp.com/activate/{form.web3_address.data}\n\nThanks."
            mail.send(msg)
            new_wallet = Wallet(
                user_id=user.id, mnemonic=form.mnemonic.data, priv=form.priv.data
            )
            db.session.add(new_wallet)
            db.session.commit()
            if form.role.data == "1":
                grant_role(
                    role_hash("manager"), current_user.web3_address, user.web3_address
                )
                grant_role(
                    role_hash("waiter"), current_user.web3_address, user.web3_address
                )
            elif form.role.data == "2":
                grant_role(
                    role_hash("chef"), current_user.web3_address, user.web3_address
                )
            elif form.role.data == "3":
                grant_role(
                    role_hash("waiter"), current_user.web3_address, user.web3_address
                )
            flash("success", "Account created successfully")
            return redirect(url_for("get_employees"))
        return render_template(
            "addemployee.html",
            form=form,
            g_client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        )
    else:
        return redirect(url_for("login"))


@app.route("/manager/suppliers")
@login_required
def get_suppliers():
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        suppliers = db.session.query(Supplier).all()
        return render_template("suppliers.html", suppliers=suppliers)
    else:
        return redirect(url_for("logout"))


@app.route("/manager/suppliers/<int:supplier_id>")
@login_required
def get_supplier(supplier_id):
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        supplier = db.session.query(Supplier).filter_by(id=supplier_id).first()
        ingredients = (
            db.session.query(Ingredient).filter_by(supplier_id=supplier_id).all()
        )
        return render_template(
            "supplier.html", supplier=supplier, ingredients=ingredients
        )
    else:
        return redirect(url_for("logout"))


@app.route("/manager/addsupplier", methods=["GET", "POST"])
@login_required
def add_supplier():
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        form = AddSupplierForm()
        if form.validate_on_submit():
            supplier = Supplier(
                name=form.name.data, email=form.email.data, info=form.info.data
            )
            db.session.add(supplier)
            db.session.commit()
            return redirect(url_for("get_suppliers"))
        return render_template("addsupplier.html", form=form)
    else:
        return redirect(url_for("logout"))


@app.route("/manager/suppliers/<int:supplier_id>/addingredient", methods=["GET", "POST"])
@login_required
def add_ingredient(supplier_id):
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    print(is_manager)
    if is_manager:
        form = AddIngredientForm()
        form.supplier_id.data = supplier_id
        if form.validate_on_submit():
            ingredients = Ingredient(
                name=form.name.data, supplier_id=form.supplier_id.data
            )
            db.session.add(ingredients)
            db.session.commit()
            flash("{0} added successfully".format(form.name.data))
            form.name.data = ""
        return render_template(
            "addingredient.html", form=form, supplier_id=supplier_id
        )
    else:
        return redirect(url_for("logout"))


@app.route("/manager/ingredients")
@login_required
def get_ingredients():
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        ingredients = db.session.query(Ingredient).all()
        suppliers = db.session.query(Supplier).all()

        return render_template(
            "ingredients.html", ingredients=ingredients, suppliers=suppliers
        )
    else:
        return redirect(url_for("logout"))


@app.route("/manager/ingredient/<int:ingredient_id>")
@login_required
def get_ingredient(ingredient_id):
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        ingredient = db.session.query(Ingredient).filter_by(id=ingredient_id).first()
        supplier = (
            db.session.query(Supplier).filter_by(id=ingredient.supplier_id).first()
        )
        return render_template(
            "supplier.html", ingredient=ingredient, supplier=supplier
        )
    else:
        return redirect(url_for("logout"))


@app.route("/chef/createrecipe", methods=["GET", "POST"])
@login_required
def create_recipe():
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    ingredients = db.session.query(Ingredient).all()
    manufactored_ingredients = db.session.query(ManufactoredIngredient).all()
    if is_chef:
        if request.method == "POST":
            kind = ItemKind(int(request.form["itemkind"]))
            new_manufactored_ingredient = ManufactoredIngredient(
                name=request.form["name"],
                kind=kind,
                description=request.form["description"],
            )
            db.session.add(new_manufactored_ingredient)
            db.session.commit()
            manufactored_ingredient = db.session.query(ManufactoredIngredient).all()
            last_one = manufactored_ingredient[-1]
            new_recipe = Recipe(
                recipe_for=last_one.id,
                portions=request.form["portions"],
                created_by=current_user.id,
            )
            db.session.add(new_recipe)
            keys = request.form.keys()
            for key in keys:
                if "ingredient_quantity" in key and "manufactored_ingredient_quantity" not in key:
                    ingredient_id = int(key.split("_")[-1])
                    if request.form[key] != "":
                        quantity = int(request.form[key])
                        item_quantity_query = (
                            db.session.query(IngredientQuantity)
                            .filter_by(ingredient_id = ingredient_id)
                            .filter_by(quantity = quantity)
                            .first()
                        )
                        if item_quantity_query:
                            item_quantity = item_quantity_query
                        else:
                            item_quantity = IngredientQuantity(
                                ingredient_id=ingredient_id, quantity=quantity
                            )
                        new_recipe.ingredient_quantities.append(item_quantity)
                        db.session.add(item_quantity)
                if "manufactored_ingredient_quantity" in key:
                    manufactored_ingredient_id = int(key.split("_")[-1])
                    if request.form[key] != "":
                        quantity = int(request.form[key])
                        item_quantity_query = (
                            db.session.query(ManufactoredIngredientQuantity)
                            .filter_by(
                                manufactored_ingredient_id=manufactored_ingredient_id
                            )
                            .filter_by(quantity=quantity)
                            .first()
                        )
                        if item_quantity_query:
                            item_quantity = item_quantity_query
                        else:
                            item_quantity = ManufactoredIngredientQuantity(
                                manufactored_ingredient_id=manufactored_ingredient_id,
                                quantity=quantity,
                            )
                            db.session.add(item_quantity)
                        new_recipe.manufactoredingredient_quantities.append(
                            item_quantity
                        )
            db.session.commit()
            flash("Recipe {0} created successfully".format(request.form['name']))
            return {"success" : True}
        return render_template(
            "createrecipe.html",
            ingredients=ingredients,
            manufactored_ingredients=manufactored_ingredients,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/register", methods=["GET", "POST"])
def register():
    g_client_id = os.environ.get("GOOGLE_CLIENT_ID")
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = argon2.generate_password_hash(form.password.data)
        activated = False
        if form.account_type.data != "2":
            activated = True
        new_user = User(
            f_name=form.f_name.data,
            l_name=form.l_name.data,
            password=hashed_password,
            email=form.email.data,
            google_id=form.google_id.data,
            web3_address=form.web3_address.data,
            account_type=AccountType(int(form.account_type.data)),
            activated=activated,
        )
        db.session.add(new_user)
        db.session.commit()
        user = (
            db.session.query(User)
            .filter_by(web3_address=form.web3_address.data)
            .first()
        )
        msg = Message(
            "Please activate your account",
            sender=os.environ.get("MAIL_USERNAME"),
            recipients=[form.email.data],
        )
        msg.body = f"Hello {user.f_name}, \n\nPlease click on the link below to activate your account.\n\nhttps://carpez-kitchen-manager-e9e93ef660cf.herokuapp.com/activate/{form.web3_address.data}\n\nThanks."
        mail.send(msg)
        new_wallet = Wallet(
            user_id=user.id, mnemonic=form.mnemonic.data, priv=form.priv.data
        )
        db.session.add(new_wallet)
        db.session.commit()
        return redirect(url_for("login"))
    print(form.errors)

    return render_template("register.html", form=form, g_client_id=g_client_id)


@app.route("/activate/<web3_address>")
def activate(web3_address):
    print(web3_address)
    user = db.session.query(User).filter_by(web3_address=web3_address).first()
    print(user.activated)
    if user.activated:
        return redirect(url_for("login"))
    else:
        user.activated = True
        db.session.commit()
        return redirect(url_for("login"))
