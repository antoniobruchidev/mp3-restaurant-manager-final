import os
import datetime
from flask import flash, jsonify, redirect, render_template, request, url_for
from restaurantmanager import app, db, argon2, mail, ALLOWED_EXTENSIONS
from restaurantmanager.models import (
    AccountType,
    Board,
    BoardMessage,
    BoardMessageReply,
    ItemKind,
    PlacedOrder,
    StockManagement,
    User,
    Wallet,
    Supplier,
    Ingredient,
    ManufactoredIngredient,
    IngredientQuantity,
    ManufactoredIngredientQuantity,
    Recipe,
    StockMovement,
    Order,
    Delivery,
    recipe_ingredientquantity,
    recipe_manufactoredingredientquantity,
    placedorder_ingredientquantity,
    placedorder_ingredientquantity,
    delivery_ingredientquantity,
    stockmovement_ingredientquantity,
    stockmovement_manufactoredingredientquantity,
    order_manufactoredingredientquantity,
)
from restaurantmanager.middleware import (
    append_ingredient_quantity,
    append_manufactored_ingredient_quantity,
    calculate_preparation_quantities,
    decrease_stock,
    decrease_stock_manufactored,
    get_ingredient_quantity_from_form,
    get_ingredient_related_deliveries,
    get_ingredient_related_placedorders,
    get_ingredient_related_recipes,
    get_ingredient_related_stockmovements,
    get_manufactored_ingredient_quantity_from_form,
    get_manufactored_ingredient_related_orders,
    get_manufactored_ingredient_related_stockmovements,
    increase_stock,
    increase_stock_manufactored,
    update_ingredient_quantity,
    update_manufactored_ingredient_quantity,
)
from flask_login import (
    AnonymousUserMixin,
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
    AnswerMessageForm,
    CreateMessageForm,
    LoginForm,
    RegisterForm,
)
from restaurantmanager.web3interface import w3, check_role, grant_role, role_hash
from flask_mail import Message
from werkzeug.utils import secure_filename


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def menu():
    """
    Route to list the menu page, if an item is sellable
    it will go in the menu"""
    starters = (
        db.session.query(ManufactoredIngredient)
        .filter(
            ManufactoredIngredient.sellable_item == True,
            ManufactoredIngredient.kind == ItemKind(1),
        )
        .all()
    )
    mains = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.main)
        .all()
    )
    desserts = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.dessert)
        .all()
    )
    pizzas = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.pizza)
        .all()
    )
    pastas = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.pasta)
        .all()
    )
    water = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.water)
        .all()
    )
    soft_drinks = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.soft_drinks)
        .all()
    )
    juices = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.juice)
        .all()
    )
    wines = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.wine)
        .all()
    )
    beers = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.beer)
        .all()
    )
    distillates = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.distillates)
        .all()
    )
    return render_template(
        "menu.html",
        starters=starters,
        mains=mains,
        desserts=desserts,
        pizzas=pizzas,
        pastas=pastas,
        water=water,
        soft_drinks=soft_drinks,
        juices=juices,
        wines=wines,
        beers=beers,
        distillates=distillates,
        logged_out=True,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for login
    """
    g_client_id = os.environ.get("GOOGLE_CLIENT_ID")
    if request.method == "POST":
        if request.form["account_type"] == "3":
            user = (
                db.session.query(User)
                .filter_by(google_id=request.form["google_id"])
                .first()
            )

            if user:
                logged_in = User.query.filter_by(
                    google_id=request.form["google_id"]
                ).first()
                login_user(logged_in)
                return {"success": True}
            else:
                return redirect(url_for("login"))
        elif request.form["account_type"] == "2":
            user = db.session.query(User).filter_by(
                email=request.form["email"]
            ).first()
            if user:
                if user.activated:
                    if argon2.check_password_hash(
                        user.password, request.form["password"]
                    ):
                        logged_in = User.query.filter_by(
                            email=request.form["email"]
                        ).first()
                    login_user(logged_in)
                    return {"success": True}
                else:
                    return redirect(url_for("login"))
            else:
                return redirect(url_for("login"))
        elif request.form["account_type"] == "1":
            user = (
                db.session.query(User)
                .filter_by(web3_address=request.form["web3_address"])
                .first()
            )
            if user:
                logged_in = User.query.filter_by(
                    web3_address=request.form["web3_address"]
                ).first()
                login_user(logged_in)
                return {"success": True}
            else:
                return redirect(url_for("login"))
    return render_template(
        "login.html",
        g_client_id=g_client_id,
        logged_out=True
    )


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Route for dashboard
    """
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
        db.session.query(BoardMessage).filter_by(
            sender_id=current_user.id
        ).all()
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
        my_messages=my_messages,
    )


@app.route("/logout")
@login_required
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for("login"))


@app.route("/messageboard")
@login_required
def messageboard():
    """messageboard route"""
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
            db.session.query(BoardMessage).filter_by(
                board=Board.manager
            ).all()
        )
    else:
        manager_messages = []
    if is_chef:
        chef_messages = db.session.query(BoardMessage).filter_by(
            board=Board.chef
        ).all()
    else:
        chef_messages = []
    if is_waiter:
        waiter_messages = (
            db.session.query(BoardMessage).filter_by(
                board=Board.waiter
            ).all()
        )
    else:
        waiter_messages = []
    public_messages = db.session.query(BoardMessage).filter_by(
        board=Board.public
    ).all()
    board_messages = (
        owner_messages
        + manager_messages
        + chef_messages
        + waiter_messages
        + public_messages
    )

    return render_template(
        "messageboard.html",
        board_messages=board_messages,
        is_manager=is_manager,
        is_chef=is_chef,
        is_waiter=is_waiter,
    )


@app.route("/messageboards/sendmessage", methods=["GET", "POST"])
@login_required
def sendmessage():
    """Route for sending message"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    date = datetime.datetime.now()
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
    return render_template(
        "sendmessage.html",
        form=form,
        is_manager=is_manager,
        is_chef=is_chef,
        is_waiter=is_waiter,
    )


@app.route("/messageboards/<int:message_id>/answer", methods=["GET", "POST"])
@login_required
def answer_message(message_id):
    """Route to answer messages"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    board_message = db.session.query(BoardMessage).filter_by(
        id=message_id
    ).first()
    if board_message:
        date = datetime.datetime.now()
        form = AnswerMessageForm()
        if form.validate_on_submit():
            answer_message = BoardMessageReply(
                reply=form.answer.data,
                message_id=board_message.id,
                timestamp=date
            )
            db.session.add(answer_message)
            db.session.commit()
            board_message.replies.append(answer_message)
            db.session.commit()
            flash("Your reply has been sent")
            return redirect(url_for("messageboard"))
        return render_template(
            "answermessage.html",
            form=form,
            is_manager=is_manager,
            is_chef=is_chef,
            is_waiter=is_waiter,
        )
    else:
        flash("You cannot answer this message")
        return redirect(url_for("messageboard"))


@app.route("/messageboards/<int:message_id>/delete", methods=["GET", "POST"])
@login_required
def delete_message(message_id):
    """route to delete a message"""
    board_message = db.session.query(BoardMessage).filter_by(
        id=message_id
    ).first()
    if board_message:
        if board_message.sender_id == current_user.id:
            for reply in board_message.replies:
                db.session.delete(reply)
            db.session.delete(board_message)
            db.session.commit()
            flash("Your message has been deleted")
            return redirect(url_for("messageboard"))
        else:
            flash("You cannot delete this message")
            return redirect(url_for("messageboard"))
    else:
        flash("You cannot delete this message")
        return redirect(url_for("messageboard"))


@app.route("/manager/staff")
@login_required
def get_employees():
    """route to get employees"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        employees = db.session.query(User).filter_by(roles=True).all()
        managers = []
        chefs = []
        waiters = []

        for employee in employees:
            manager = check_role(role_hash("manager"), employee.web3_address)
            chef = check_role(role_hash("chef"), employee.web3_address)
            waiter = check_role(role_hash("waiter"), employee.web3_address)
            managers.append(manager)
            chefs.append(chef)
            waiters.append(waiter)
        staff_data = list(zip(employees, managers, chefs, waiters))
        return render_template("staff.html", staff_data=staff_data)
    else:
        return redirect(url_for("dashboard"))


@app.route("/manager/addemployee", methods=["GET", "POST"])
@login_required
def add_employee():
    """Route to add an employee from the registered users"""
    is_owner = check_role(role_hash("owner"), current_user.web3_address)
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    users = db.session.query(User).all()
    users_data = []
    for user in users:
        users_data.append(
            {
                "id": user.id,
                "title": f"{user.f_name} {user.l_name}",
                "web3_address": user.web3_address,
            }
        )
    if is_owner or is_manager:
        if request.method == "POST":
            role_id = request.form["role"]
            user_id = request.form["id"]
            user = db.session.query(User).filter_by(id=user_id).first()
            if role_id == "1":
                assert grant_role(
                    role_hash("manager"),
                    current_user.web3_address,
                    user.web3_address
                )
            elif role_id == "2":
                assert grant_role(
                    role_hash("chef"),
                    current_user.web3_address,
                    user.web3_address
                )
            elif role_id == "3":
                assert grant_role(
                    role_hash("waiter"),
                    current_user.web3_address,
                    user.web3_address
                )
            user.roles = True
            db.session.add(user)
            db.session.commit()
            flash("success", "Account created successfully")
            return {"success": True}
        return render_template(
            "addemployee.html",
            is_owner=is_owner,
            is_manager=is_manager,
            users=users_data,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/suppliers")
@login_required
def get_suppliers():
    """route to list the suppliers"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        suppliers = db.session.query(Supplier).all()
        return render_template(
            "suppliers.html", suppliers=suppliers, is_manager=is_manager
        )
    else:
        return redirect(url_for("logout"))


@app.route("/suppliers/<int:supplier_id>")
@login_required
def get_supplier(supplier_id):
    """route to list a supplier data and the ingredients bought from them"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        supplier = db.session.query(Supplier).filter_by(
            id=supplier_id
        ).first()
        ingredients = (
            db.session.query(Ingredient).filter_by(
                supplier_id=supplier_id
            ).all()
        )
        return render_template(
            "supplier.html",
            supplier=supplier,
            ingredients=ingredients,
            is_manager=is_manager,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/suppliers/addsupplier", methods=["GET", "POST"])
@login_required
def add_supplier():
    """route to add a supplier"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    if is_manager or is_chef:
        form = AddSupplierForm()
        if form.validate_on_submit():
            supplier = Supplier(
                name=form.name.data,
                email=form.email.data,
                info=form.info.data
            )
            db.session.add(supplier)
            db.session.commit()
            return redirect(url_for("get_suppliers"))
        return render_template(
            "addsupplier.html",
            form=form,
            is_manager=is_manager
        )
    else:
        flash("Only managers and chefs can add supliers")
        return redirect(url_for("dashboard"))


@app.route(
    "/suppliers/<int:supplier_id>/addingredient",
    methods=["GET", "POST"]
)
@login_required
def add_ingredient(supplier_id):
    """route to add an ingredient to a given supplier"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    if is_manager or is_chef:
        form = AddIngredientForm()
        form.supplier_id.data = supplier_id
        supplier = db.session.query(Supplier).filter_by(
            id=supplier_id
        ).first()
        if form.validate_on_submit():
            ingredients = Ingredient(
                name=form.name.data,
                supplier_id=form.supplier_id.data,
                description=form.description.data,
            )
            db.session.add(ingredients)
            db.session.commit()
            flash("{0} added successfully".format(form.name.data))
            form.name.data = ""
        return render_template(
            "addingredient.html",
            form=form,
            supplier=supplier,
            is_manager=is_manager
        )
    else:
        flash("Only managers and chefs can add an ingredient")
        return redirect(url_for("dashboard"))


@app.route(
    "/suppliers/<int:supplier_id>/ingredients/<ingredient_id>/delete",
    methods=["GET"]
)
@login_required
def delete_ingredient(supplier_id, ingredient_id):
    """route to delete an ingredient from the supplier"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        ingredient = db.session.query(Ingredient).filter_by(
            id=ingredient_id
        ).first()
        db.session.delete(ingredient)
        db.session.commit()
        flash("Ingredient removed successfully")
        return redirect(url_for("get_supplier", supplier_id=supplier_id))
    else:
        flash("Only managers can delete ingredients")
        return redirect(url_for("dashboard"))


@app.route("/manager/placedorders")
@login_required
def get_all_placedorders():
    """route to list all the placed orders"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        orders = db.session.query(PlacedOrder).all()
        suppliers = []
        for order in orders:
            supplier = (
                db.session.query(Supplier).filter_by(
                    id=order.supplier_id
                ).first()
            )
            suppliers.append(supplier)
        orders_data = list(zip(orders, suppliers))
        return render_template(
            "placedorders.html",
            orders_data=orders_data,
            is_manager=is_manager,
            is_chef=is_chef,
            is_waiter=is_waiter,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/suppliers/<supplier_id>/placedorders")
@login_required
def get_placedorders(supplier_id):
    """route to list the placed orders from a given supplier"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        supplier = db.session.query(Supplier).filter_by(
            id=order.supplier_id
        ).first()
        orders = db.session.query(PlacedOrder).filter_by(
            supplier_id=supplier_id
        ).all()
        suppliers = []
        for order in orders:
            suppliers.append(supplier)
        orders_data = list(zip(orders, suppliers))
        return render_template(
            "placedorders.html",
            orders_data=orders_data,
            is_manager=is_manager,
            is_chef=is_chef,
            is_waiter=is_waiter,
        )
    else:
        return redirect(url_for("logout"))


@app.route(
    "/suppliers/<int:supplier_id>/placedorders/<int:order_id>/view-placedorder"
)
@login_required
def get_placedorder(supplier_id, order_id):
    """route to see a single placed order info"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if order_id == 0:
        if is_manager or is_chef or is_waiter:
            placedorder = (
                db.session.query(PlacedOrder)
                .filter_by(id=supplier_id)
                .filter_by(sent=False)
                .first()
            )
            ingredients = (
                db.session.query(Ingredient).filter_by(
                    supplier_id=supplier_id
                ).all()
            )
            ingredients_in_order = []
            if placedorder != None:
                for ingredient_quantity in placedorder.ingredient_quantities:
                    ingredient = (
                        db.session.query(Ingredient)
                        .filter_by(id=ingredient_quantity.ingredient_id)
                        .first()
                    )
                    ingredients_in_order.append(ingredient)
                return render_template(
                    "placedorder.html",
                    placedorder=placedorder,
                    ingredients=ingredients,
                    ingredients_in_order=ingredients_in_order,
                    is_manager=is_manager,
                    is_chef=is_chef,
                )
            else:
                return render_template(
                    "placedorder.html",
                    supplier_id=supplier_id,
                    placedorder=None,
                    ingredients=ingredients,
                    is_manager=is_manager,
                    is_chef=is_chef,
                )
        else:
            return redirect(url_for("logout"))
    else:
        placedorder = db.session.query(PlacedOrder).filter_by(
            id=order_id
        ).first()
        ingredients = (
            db.session.query(Ingredient).filter_by(
                supplier_id=supplier_id
            ).all()
        )
        ingredients_in_order = []
        if placedorder != None:
            for ingredient_quantity in placedorder.ingredient_quantities:
                ingredient = (
                    db.session.query(Ingredient)
                    .filter_by(id=ingredient_quantity.ingredient_id)
                    .first()
                )
                ingredients_in_order.append(ingredient)
            return render_template(
                "placedorder.html",
                placedorder=placedorder,
                ingredients=ingredients,
                ingredients_in_order=ingredients_in_order,
                is_manager=is_manager,
                is_chef=is_chef,
            )


@app.route("/placedorders/<order_id>/send", methods=["POST"])
@login_required
def send_order(order_id):
    """
    route to flag an order as sent, it has to be done manually
    depending from the supplier preference
    """
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        order = db.session.query(PlacedOrder).filter_by(id=order_id).first()
        order.sent = True
        # TODO: send order to supplier via email
        db.session.add(order)
        db.session.commit()
        flash("Order saved successfully as sent")
        return {"success": True}
    else:
        flash("Only managers can send an order")
        return redirect(url_for("dashboard"))


@app.route("/suppliers/<supplier_id>/add_to_order", methods=["POST"])
@login_required
def add_to_order(supplier_id):
    """route to add ingredients to an order"""
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        if request.method == "POST":
            open_order = (
                db.session.query(PlacedOrder)
                .filter_by(supplier_id=supplier_id)
                .filter_by(sent=False)
                .first()
            )
            if open_order == None:
                open_order = PlacedOrder(
                    supplier_id=supplier_id,
                    sent=False,
                    dateTime=datetime.datetime.now(),
                )
            db.session.add(open_order)
            db.session.commit()
            open_order = (
                db.session.query(PlacedOrder)
                .filter_by(supplier_id=supplier_id)
                .filter_by(sent=False)
                .first()
            )
            ingredient_quantites = get_ingredient_quantity_from_form(
                request.form.keys(), request.form
            )
            assert append_ingredient_quantity(
                ingredient_quantites,
                open_order
            )
            db.session.commit()
            flash("Item added to order successfully")
            return {"success": True}
    else:
        return redirect(url_for("logout"))


@app.route("/deliveries")
@login_required
def get_all_deliveries():
    """route to list all deliveries"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        deliveries = db.session.query(Delivery).all()
        suppliers = []
        for delivery in deliveries:
            supplier = (
                db.session.query(Supplier).filter_by(
                    id=delivery.supplier_id
                ).first()
            )
            suppliers.append(supplier)
        deliveries_data = list(zip(deliveries, suppliers))
        return render_template(
            "deliveries.html",
            deliveries_data=deliveries_data,
            is_manager=is_manager,
            is_chef=is_chef,
            is_waiter=is_waiter,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/deliveries/suppliers/<supplier_id>")
@login_required
def get_deliveries(supplier_id):
    """route to list deliveries from a given supplier"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        supplier = db.session.query(Supplier).filter_by(
            id=supplier_id
        ).first()
        suppliers = []
        deliveries = db.session.query(Delivery).filter_by(
            supplier_id=supplier_id
        ).all()
        for delivery in deliveries:
            suppliers.append(supplier)
        deliveries_data = list(zip(deliveries, suppliers))
        return render_template(
            "deliveries.html",
            deliveries_data=deliveries_data,
            is_manager=is_manager,
            is_chef=is_chef,
            is_waiter=is_waiter,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/suppliers/<supplier_id>/deliveries/<delivery_id>")
@login_required
def get_delivery(supplier_id, delivery_id):
    """route to list a single delivery info"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        delivery = db.session.query(Delivery).filter_by(
            id=delivery_id
        ).first()
        ingredients = []
        quantities = []
        if delivery != None:
            for ingredient_quantity in delivery.ingredient_quantities:
                ingredient = (
                    db.session.query(Ingredient)
                    .filter_by(id=ingredient_quantity.ingredient_id)
                    .first()
                )
                ingredients.append(ingredient)
                quantities.append(ingredient_quantity.quantity)
            supplier = (
                db.session.query(Supplier).filter_by(
                    id=delivery.supplier_id
                ).first()
            )
            return render_template(
                "delivery.html",
                delivery=delivery,
                supplier=supplier,
                ingredients=ingredients,
                quantities=quantities,
                is_manager=is_manager,
                is_chef=is_chef,
            )
        else:
            return render_template("delivery.html", delivery=None)
    else:
        return redirect(url_for("logout"))


@app.route(
    "/suppliers/<int:supplier_id>/deliveries/adddelivery",
    methods=["GET", "POST"]
)
@login_required
def add_delivery(supplier_id):
    """route to add a delivery to a given supplier"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    ingredients = db.session.query(Ingredient).filter_by(
        supplier_id=supplier_id
    ).all()
    if is_manager or is_chef or is_waiter:
        if request.method == "POST":
            delivery = Delivery(
                supplier_id=supplier_id,
                date=datetime.datetime.now(),
                user_id=current_user.id,
                info=request.form["info"],
                supplier_reference=request.form["supplier_reference"],
            )
            db.session.add(delivery)
            db.session.commit()
            keys = request.form.keys()
            ingredient_quantities = get_ingredient_quantity_from_form(
                keys, request.form
            )
            assert append_ingredient_quantity(ingredient_quantities, delivery)
            assert increase_stock(ingredient_quantities)
            db.session.commit()
            flash("Delivery placed successfully")
            return {"success": True}
        else:
            return render_template(
                "adddelivery.html",
                supplier_id=supplier_id,
                ingredients=ingredients
            )
    else:
        return redirect(url_for("logout"))


@app.route("/manager/recipes")
@login_required
def get_all_recipes():
    """route to list all recipes"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    if is_manager or is_chef:
        recipes = db.session.query(Recipe).all()
        recipes_for = []
        for recipe in recipes:
            recipe_for = (
                db.session.query(ManufactoredIngredient)
                .filter_by(id=recipe.recipe_for)
                .first()
            )
            recipes_for.append(recipe_for)
        return render_template(
            "recipes.html",
            recipes=recipes,
            recipes_for=recipes_for,
            is_manager=is_manager,
            is_chef=is_chef,
            kind=ItemKind,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/manager/recipes/<recipe_id>")
@login_required
def get_recipe(recipe_id):
    """route lo list a given recipe info"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    all_ingredients = db.session.query(Ingredient).all()
    all_manufactored_ingredients = db.session.query(
        ManufactoredIngredient
    ).all()
    ingredients_data = []
    for ingredient in all_ingredients:
        ingredients_data.append({
            "name": ingredient.name,
            "id": ingredient.id,
            "manufactored": False
        })
    for manufactored_ingredient in all_manufactored_ingredients:
        ingredients_data.append(
            {
                "name": manufactored_ingredient.name,
                "id": manufactored_ingredient.id,
                "manufactored": True,
            }
        )
    if is_manager or is_chef:
        recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
        item = (
            db.session.query(ManufactoredIngredient)
            .filter_by(id=recipe.recipe_for)
            .first()
        )
        ingredients = []
        manufactored_ingredients = []
        for ingredient_quantity in recipe.ingredient_quantities:
            ingredient = (
                db.session.query(Ingredient)
                .filter_by(id=ingredient_quantity.ingredient_id)
                .first()
            )
            ingredients.append(ingredient)
        for m_i_q in recipe.manufactoredingredient_quantities:
            manufactored_ingredient = (
                db.session.query(ManufactoredIngredient)
                .filter_by(
                    id=m_i_q.manufactored_ingredient_id
                )
                .first()
            )
            manufactored_ingredients.append(manufactored_ingredient)
        return render_template(
            "recipe.html",
            recipe=recipe,
            ingredients=ingredients,
            manufactored_ingredients=manufactored_ingredients,
            ingredients_data=ingredients_data,
            item=item,
            is_manager=is_manager,
            is_chef=is_chef,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/manager/recipes/<recipe_id>/edit", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    """route for editing a recipe"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    if is_manager or is_chef:
        recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
        m_i = (
            db.session.query(ManufactoredIngredient)
            .filter_by(id=recipe.recipe_for)
            .first()
        )
        if request.method == "POST" and is_manager:
            if request.form["name"]:
                m_i.name = request.form["name"]
            if request.form["description"]:
                m_i.description = request.form["description"]
            if request.form["sellable_item"] == "true":
                m_i.sellable_item = True
            else:
                m_i.sellable_item = False
            if request.form["price"]:
                m_i.price = request.form["price"]
            if "file_input" in request.files:
                file = request.files["file_input"]
                if file.filename != "":
                    allowed_file = (
                        "." in file.filename
                        and file.filename.rsplit(".", 1)[1].lower()
                        in ALLOWED_EXTENSIONS
                    )
                if file and allowed_file:
                    filename = secure_filename(file.filename)
                    path = app.root_path+app.config["UPLOAD_FOLDER"]+filename
                    file.save(path)
                    m_i.image = f"images/{filename}"
                    db.session.add(m_i)
                    db.session.commit()
                else:
                    flash("File format not recognized")
                    return {"success": False}
        if request.method == "POST" and is_chef:
            if request.form["portions"]:
                recipe.portions = request.form["portions"]
            keys = request.form.keys()
            ingredient_quantities = get_ingredient_quantity_from_form(
                keys, request.form
            )
            assert update_ingredient_quantity(ingredient_quantities, recipe)
            manufactored_ingredient_quantity = (
                get_manufactored_ingredient_quantity_from_form(
                    keys, request.form
                )
            )
            assert update_manufactored_ingredient_quantity(
                manufactored_ingredient_quantity, recipe
            )
        if request.method == "GET":
            return redirect(
                url_for(
                    "get_recipe",
                    recipe_id=recipe_id,
                    is_manager=is_manager,
                    is_chef=is_chef,
                )
            )
        flash("Recipe updated successfully")
        return {"success": True}
    else:
        return redirect(url_for("logout"))


@app.route("/manager/stockmanagement")
@login_required
def stockmanagement():
    """route for the stock management"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    ingredients = db.session.query(Ingredient).all()
    ingredients_data = []
    manufactored_ingredients = db.session.query(ManufactoredIngredient).all()
    for ingredient in ingredients:
        ingredients_data.append({
            "name": ingredient.name,
            "id": ingredient.id,
            "manufactored": False
            })
    for manufactored_ingredient in manufactored_ingredients:
        ingredients_data.append(
            {
                "name": manufactored_ingredient.name,
                "id": manufactored_ingredient.id,
                "manufactored": True,
            }
        )
    if is_manager or is_chef:
        return render_template(
            "stockmanagement.html",
            is_manager=is_manager,
            is_chef=is_chef,
            ingredients=ingredients_data,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/chef/createrecipe", methods=["GET", "POST"])
@login_required
def create_recipe():
    """route to create a recipe"""
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    ingredients = db.session.query(Ingredient).all()
    manufactored_ingredients = db.session.query(
        ManufactoredIngredient
    ).all()
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
            manufactored_ingredient = db.session.query(
                ManufactoredIngredient
            ).all()[-1]
            new_recipe = Recipe(
                recipe_for=manufactored_ingredient.id,
                portions=request.form["portions"],
                created_by=current_user.id,
            )
            db.session.add(new_recipe)
            db.session.commit()
            recipe = db.session.query(Recipe).all()[-1]
            keys = request.form.keys()

            ingredient_quantities = get_ingredient_quantity_from_form(
                keys, request.form
            )
            assert update_ingredient_quantity(ingredient_quantities, recipe)
            manufactored_ingredient_quantity = (
                get_manufactored_ingredient_quantity_from_form(
                    keys, request.form
                )
            )
            assert update_manufactored_ingredient_quantity(
                manufactored_ingredient_quantity, recipe
            )
            flash("Recipe {0} created successfully".format(
                request.form["name"]
            ))
            return {"success": True}
        return render_template(
            "createrecipe.html",
            ingredients=ingredients,
            manufactored_ingredients=manufactored_ingredients,
        )
    else:
        return redirect(url_for("logout"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """route to register"""
    g_client_id = os.environ.get("GOOGLE_CLIENT_ID")
    activation_link = "{}/activate".format(os.environ.get("HEROKU_DOMAIN"))
    user_delete_link = "{}/delete".format(os.environ.get("HEROKU_DOMAIN"))
    if request.method == "POST":
        hashed_password = argon2.generate_password_hash(
            request.form["password"]
        )
        activated = True
        if request.form["account_type"] == "2":
            activated = False
        new_user = User(
            f_name=request.form["f_name"],
            l_name=request.form["l_name"],
            password=hashed_password,
            email=request.form["email"],
            google_id=request.form["google_id"],
            web3_address=request.form["web3_address"],
            account_type=AccountType(int(request.form["account_type"])),
            activated=activated,
        )
        db.session.add(new_user)
        db.session.commit()
        user = (
            db.session.query(User)
            .filter_by(web3_address=request.form["web3_address"])
            .first()
        )
        if request.form["account_type"] == "2":
            msg = Message(
                "Please activate your account",
                sender=os.environ.get("MAIL_USERNAME"),
                recipients=[request.form["email"]],
            )
            msg.body = (
                f"Hello {user.f_name},\n\n"
                f"please click on the link below to activate your account.\n\n"
                f"{activation_link}/{user.web3_address}\n\n"
                "Thanks."
            )
            mail.send(msg)
        elif request.form["account_type"] == "3":
            msg = Message(
                "Registration Confirmation",
                sender=os.environ.get("MAIL_USERNAME"),
                recipients=[request.form["email"]],
            )
            msg.body = (
                f"Hello {user.f_name},\n\n"
                "You just registered on Carpez Kitchen. If it wasn't you \
                or you changed your mind please the link below.\n\n"
                f"{user_delete_link}/{user.web3_address}\n\n"
                "Thanks."
            )
            mail.send(msg)
        new_wallet = Wallet(
            user_id=user.id,
            mnemonic=request.form["mnemonic"],
            priv=request.form["priv"],
        )
        db.session.add(new_wallet)
        db.session.commit()
        return {"success": True}
    form = request.form
    return render_template(
        "register.html", form=form, g_client_id=g_client_id, logged_out=True
    )


@app.route("/activate/<web3_address>")
def activate(web3_address):
    """route to activate user"""
    print(web3_address.lower())
    user = db.session.query(User).filter_by(web3_address=web3_address).first()
    print(user.activated)
    if user.activated:
        return redirect(url_for("login"))
    else:
        user.activated = True
        db.session.commit()
        return redirect(url_for("login"))


@app.route("/api/ingredients/<int:id>/get_ingredient_data")
def get_ingredient_data(id):
    """route to get all data related to a given ingredient"""
    ingredient = db.session.query(Ingredient).filter_by(id=id).first()
    ingredient_data = {
        "name": ingredient.name,
        "ingredient_id": ingredient.id,
        "description": ingredient.description,
        "stock": ingredient.stock_in_weight,
        "supplier_id": ingredient.supplier_id,
    }
    related_ingredientquantities = (
        db.session.query(IngredientQuantity).filter_by(ingredient_id=id).all()
    )
    recipe_ids = []
    for related_ingredientquantity in related_ingredientquantities:
        related_recipes = (
            db.session.query(recipe_ingredientquantity)
            .filter_by(ingredient_quantity_id=related_ingredientquantity.id)
            .all()
        )
        for recipe in related_recipes:
            if recipe != None:
                recipe_ids.append(recipe.recipe_id)
    placedorder_ids = []
    for related_ingredientquantity in related_ingredientquantities:
        related_placedorders = (
            db.session.query(placedorder_ingredientquantity)
            .filter_by(ingredient_quantity_id=related_ingredientquantity.id)
            .all()
        )
        for placedorder in related_placedorders:
            print(placedorder, placedorder.placedorder_id)
            if placedorder != None:
                placedorder_ids.append(placedorder.placedorder_id)
    delivery_ids = []
    for related_ingredientquantity in related_ingredientquantities:
        related_deliveries = (
            db.session.query(delivery_ingredientquantity)
            .filter_by(ingredient_quantity_id=related_ingredientquantity.id)
            .all()
        )
        for related_delivery in related_deliveries:
            if related_delivery != None:
                delivery_ids.append(related_delivery.delivery_id)
    stockmovement_ids = []
    for related_ingredientquantity in related_ingredientquantities:
        related_stockmovements = (
            db.session.query(stockmovement_ingredientquantity)
            .filter_by(ingredient_quantity_id=related_ingredientquantity.id)
            .all()
        )
        for related_stockmovement in related_stockmovements:
            if related_stockmovement != None:
                stockmovement_ids.append(
                    related_stockmovement.stockmovement_id
                )
    recipe_ids = list(set(recipe_ids))
    placedorder_ids = list(set(placedorder_ids))
    delivery_ids = list(set(delivery_ids))
    stockmovement_ids = list(set(stockmovement_ids))
    ingredient_related_recipes_data = get_ingredient_related_recipes(
        recipe_ids
    )
    ingredient_related_placeorders_data = get_ingredient_related_placedorders(
        placedorder_ids
    )
    ingredient_related_deliveries_data = get_ingredient_related_deliveries(
        delivery_ids
    )
    (
        ingredient_related_wastages_data,
        ingredient_related_preparations_data,
        ingredient_related_stock_takes_data,
    ) = get_ingredient_related_stockmovements(stockmovement_ids)
    print(recipe_ids, placedorder_ids, delivery_ids, stockmovement_ids)
    return {
        "ingredient": ingredient_data,
        "recipes": ingredient_related_recipes_data,
        "placedorders": ingredient_related_placeorders_data,
        "deliveries": ingredient_related_deliveries_data,
        "wastages": ingredient_related_wastages_data,
        "preparations": ingredient_related_preparations_data,
        "stock_takes": ingredient_related_stock_takes_data,
    }


@app.route("/api/manufactoredingredients/<int:id>/get_ingredient_data")
def get_manufactored_ingredient_data(id):
    """route to get all data from a given manufactored ingredient"""
    ingredient = db.session.query(ManufactoredIngredient).filter_by(
        id=id
    ).first()
    recipe = db.session.query(Recipe).filter_by(
        recipe_for=ingredient.id
    ).first()
    ingredient_data = {
        "name": ingredient.name,
        "manufactored_ingredient_id": ingredient.id,
        "description": ingredient.description,
        "stock": ingredient.stock_in_portions,
        "recipe": recipe.id,
    }
    related_ingredientquantities = (
        db.session.query(ManufactoredIngredientQuantity)
        .filter_by(manufactored_ingredient_id=id)
        .all()
    )

    recipe_ids = []
    for r_i in related_ingredientquantities:
        related_recipes = (
            db.session.query(recipe_manufactoredingredientquantity)
            .filter_by(manufactoredingredient_quantity_id=r_i.id)
            .all()
        )
        for related_recipe in related_recipes:
            if related_recipe != None:
                recipe_ids.append(related_recipe.recipe_id)
    order_ids = []
    for r_i in related_ingredientquantities:
        related_orders = (
            db.session.query(order_manufactoredingredientquantity)
            .filter_by(manufactoredingredient_quantity_id=r_i.id)
            .all()
        )
        for related_order in related_orders:
            if related_order != None:
                order_ids.append(related_order.order_id)
    stockmovement_ids = []
    for r_i in related_ingredientquantities:
        related_stockmovements = (
            db.session.query(stockmovement_manufactoredingredientquantity)
            .filter_by(manufactoredingredient_quantity_id=r_i.id)
            .all()
        )
        for related_stockmovement in related_stockmovements:
            if related_stockmovement != None:
                stockmovement_ids.append(
                    related_stockmovement.stockmovement_id
                )
            print(recipe_ids, order_ids, stockmovement_ids)
    ingredient_related_recipes_data = get_ingredient_related_recipes(
        recipe_ids
    )
    ingredient_related_orders_d = get_manufactored_ingredient_related_orders(
        order_ids
    )
    (
        ingredient_related_wastages_data,
        ingredient_related_preparations_data,
        ingredient_related_stock_takes_data,
    ) = get_manufactored_ingredient_related_stockmovements(stockmovement_ids)
    print(ingredient_related_preparations_data)
    return {
        "ingredient": ingredient_data,
        "recipes": ingredient_related_recipes_data,
        "orders": ingredient_related_orders_d,
        "wastages": ingredient_related_wastages_data,
        "preparations": ingredient_related_preparations_data,
        "stock_takes": ingredient_related_stock_takes_data,
    }


@app.route("/wastages")
@login_required
def get_wastages():
    """route to list all the recorded wastages"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        wastages = (
            db.session.query(StockMovement)
            .filter_by(preparation_kind=StockManagement(2))
            .all()
        )
        return render_template(
            "wastages.html",
            wastages=wastages,
            is_manager=is_manager,
            is_chef=is_chef,
            is_waiter=is_waiter,
        )


@app.route("/suppliers/<supplier_id>/deliveries/<delivery_id>")
@login_required
def get_wastage(wastage_id):
    """route to list a single wastage info"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_chef or is_waiter:
        wastage = db.session.query(StockMovement).filter_by(
            id=wastage_id
        ).first()
        ingredients = []
        manufactored_ingredients = []
        for ingredient_quantity in wastage.ingredient_quantities:
            ingredient = (
                db.session.query(Ingredient)
                .filter_by(id=ingredient_quantity.ingredient_id)
                .first()
            )
            ingredients.append(ingredient)
        for m_i_q in wastage.manufactoredingredient_quantities:
            manufactored_ingredient = (
                db.session.query(ManufactoredIngredient)
                .filter_by(
                    id=m_i_q.manufactored_ingredient_id
                )
                .first()
            )
            manufactored_ingredients.append(manufactored_ingredient)
            return render_template(
                "delivery.html",
                wastage=wastage,
                ingredients=ingredients,
                manufactored_ingredients=manufactored_ingredients,
                is_manager=is_manager,
                is_chef=is_chef,
            )
        else:
            return render_template("delivery.html", delivery=None)
    else:
        return redirect(url_for("logout"))


@app.route("/manager/addwastages", methods=["GET", "POST"])
@login_required
def add_wastages():
    """route to add a wastage"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    ingredients = db.session.query(Ingredient).all()
    manufactored_ingredients = db.session.query(ManufactoredIngredient).all()
    if is_manager or is_chef or is_waiter:
        if request.method == "POST":
            new_wastage = StockMovement(
                preparation_kind=StockManagement(2),
                date=datetime.datetime.now(),
                info=request.form["info"],
                employee_id=current_user.id,
            )
            keys = request.form.keys()
            ingredient_quantities = get_ingredient_quantity_from_form(
                keys, request.form
            )
            assert append_ingredient_quantity(
                ingredient_quantities, new_wastage
            )
            assert decrease_stock(ingredient_quantities)
            manufactored_ingredient_quantity = (
                get_manufactored_ingredient_quantity_from_form(
                    keys, request.form
                )
            )
            assert append_manufactored_ingredient_quantity(
                manufactored_ingredient_quantity, new_wastage
            )
            assert decrease_stock_manufactored(
                manufactored_ingredient_quantity
            )
            db.session.commit()
            flash("Wastage added successfully")
            return {"success": True}
        else:
            return render_template(
                "addwastages.html",
                ingredients=ingredients,
                manufactored_ingredients=manufactored_ingredients,
                is_manager=is_manager,
                is_waiter=is_waiter,
                is_chef=is_chef,
            )
    else:
        return redirect(url_for("logout"))


@app.route("/chef/recipes/<int:recipe_id>/prepare", methods=["GET", "POST"])
@login_required
def add_preparation(recipe_id):
    """route to add a preparation"""
    is_chef = check_role(role_hash("chef"), current_user.web3_address)
    recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
    if is_chef:
        recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()
        if request.method == "POST":
            new_preparation = StockMovement(
                preparation_kind=StockManagement(1),
                date=datetime.datetime.now(),
                info="Automated record",
                employee_id=current_user.id,
            )
            ingredient_quantity_used, manufactored_ingredient_quantity_used = (
                calculate_preparation_quantities(
                    recipe, request.form["portions"]
                )
            )
            print(recipe, request.form["portions"])
            assert decrease_stock(ingredient_quantity_used)
            assert decrease_stock_manufactored(
                manufactored_ingredient_quantity_used
            )
            ingredient_quantity_produced = ManufactoredIngredientQuantity(
                manufactored_ingredient_id=recipe.recipe_for,
                quantity=request.form["portions"],
            )
            assert increase_stock_manufactored(
                [
                    {
                        "manufactored_ingredient_id": recipe.recipe_for,
                        "quantity": ingredient_quantity_produced.quantity,
                    }
                ]
            )
            new_preparation.manufactoredingredient_quantities.append(
                ingredient_quantity_produced
            )
            db.session.add(new_preparation)
            db.session.commit()
            flash("Preparation added successfully")
            return {"success": True}
        else:
            return redirect(url_for("get_recipe", recipe_id=recipe_id))
    else:
        return redirect(url_for("logout"))


@app.route(
    "/manager/ingredients/<int:ingredient_id>/setstock", methods=["POST"]
)
@login_required
def set_ingredient_stock(ingredient_id):
    """route to manually adjust stock levels for a given ingredient"""
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        ingredient = db.session.query(Ingredient).filter_by(
            id=ingredient_id
        ).first()
        ingredient.stock_in_weight = int(request.form["stock"])
        db.session.add(ingredient)
        stockmovement = StockMovement(
            info="Manual stock take",
            employee_id=current_user.id,
            date=datetime.datetime.now(),
            preparation_kind=StockManagement(3),
        )
        db.session.add(stockmovement)
        db.session.commit()
        stock_movement = (
            db.session.query(StockMovement)
            .filter_by(info="Manual stock take")
            .all()[-1]
        )
        ingredient_quantities = [
            {
                "ingredient_id": ingredient_id,
                "quantity": int(request.form["stock"]),
            }
        ]
        assert append_ingredient_quantity(
            ingredient_quantities, stock_movement
        )
        return {"success": True}
    else:
        return redirect(url_for("logout"))


@app.route(
    "/manager/manufactoredingredients/<int:ingredient_id>/setstock",
    methods=["POST"]
)
@login_required
def set_manufactoredingredient_stock(ingredient_id):
    """
    route to manually adjust stock levels for
    a given manufactored ingredient
    """
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    if is_manager:
        ingredient = (
            db.session.query(ManufactoredIngredient).filter_by(
                id=ingredient_id
            ).first()
        )
        ingredient.stock_in_portions = int(request.form["stock"])
        db.session.add(ingredient)
        stockmovement = StockMovement(
            info="Manual stock take",
            employee_id=current_user.id,
            date=datetime.datetime.now(),
            preparation_kind=StockManagement(3),
        )
        db.session.add(stockmovement)
        db.session.commit()
        stock_movement = (
            db.session.query(StockMovement)
            .filter_by(info="Manual stock take")
            .all()[-1]
        )
        ingredient_quantities = [
            {
                "manufactored_ingredient_id": ingredient_id,
                "quantity": int(request.form["stock"]),
            }
        ]
        assert append_manufactored_ingredient_quantity(
            ingredient_quantities, stock_movement
        )
        flash("Stock updated")
        return {"success": True}
    else:
        return redirect(url_for("logout"))


@app.route("/manager/placedorders/<int:order_id>/delete")
def delete_placedorder(order_id):
    """route to delete a placed order"""
    order = db.session.query(PlacedOrder).filter_by(id=order_id).one()
    db.session.delete(order)
    db.session.commit()
    flash("Order deleted")
    return redirect(url_for("dashboard"))


@app.route("/delete/<web3_address>")
def delete_user(web3_address):
    """route to delete an user"""
    w3_cs_a = w3.to_checksum_address(web3_address)
    user = db.session.query(User).filter_by(web3_address=w3_cs_a).one()
    db.session.delete(user)
    db.session.commit()
    flash("Successfully deleted user")
    return redirect(url_for("menu"))


@app.route("/table")
def table():
    """route to table management"""
    if current_user is not AnonymousUserMixin:
        is_manager = check_role(
            role_hash("manager"), current_user.web3_address
        )
        is_chef = check_role(role_hash("chef"), current_user.web3_address)
        is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
        if is_manager or is_chef or is_waiter:
            return redirect("tables")
        else:
            return render_template("table.html")
    return render_template("table.html")


@app.route("/tables")
@login_required
def tables_management():
    """route to list every open table"""
    open_tables = db.session.query(Order).filter_by(paid=False).all()
    totals = []
    for table in open_tables:
        total = 0
        for m_i_q in table.manufactoredingredient_quantities:
            manufactored_ingredient = (
                db.session.query(ManufactoredIngredient)
                .filter_by(
                    id=m_i_q.manufactored_ingredient_id
                )
                .first()
            )
            total += (
                manufactored_ingredient.price * m_i_q.quantity
            )
        totals.append(total)
    orders_data = list(zip(open_tables, totals))
    return render_template("table_management.html", orders_data=orders_data)


@app.route("/tables/<table_number>", methods=["GET", "POST"])
def table_management(table_number):
    starters = (
        db.session.query(ManufactoredIngredient)
        .filter(
            ManufactoredIngredient.sellable_item == True,
            ManufactoredIngredient.kind == ItemKind(1),
        )
        .all()
    )
    mains = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.main)
        .all()
    )
    desserts = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.dessert)
        .all()
    )
    pizzas = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.pizza)
        .all()
    )
    pastas = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.pasta)
        .all()
    )
    water = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.water)
        .all()
    )
    soft_drinks = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.soft_drinks)
        .all()
    )
    juices = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.juice)
        .all()
    )
    wines = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.wine)
        .all()
    )
    beers = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.beer)
        .all()
    )
    distillates = (
        db.session.query(ManufactoredIngredient)
        .filter_by(sellable_item=True)
        .filter_by(kind=ItemKind.distillates)
        .all()
    )
    if request.method == "POST":
        keys = request.form.keys()
        print(request.form)
        manufactored_ingredient_quantity = (
            get_manufactored_ingredient_quantity_from_form(keys, request.form)
        )
        open_table = Order(
            dateTime=datetime.datetime.now(), paid=False, table=table_number
        )
        db.session.add(open_table)
        db.session.commit()
        open_table = (
            db.session.query(Order)
            .filter_by(paid=False)
            .filter_by(table=table_number)
            .first()
        )
        assert update_manufactored_ingredient_quantity(
            manufactored_ingredient_quantity, open_table
        )
        flash("Order add successfully at table".format(table_number))
        return {"success": True}
    else:
        return render_template(
            "menu_at_table.html",
            table_number=table_number,
            starters=starters,
            mains=mains,
            desserts=desserts,
            pizzas=pizzas,
            pastas=pastas,
            water=water,
            soft_drinks=soft_drinks,
            juices=juices,
            wines=wines,
            beers=beers,
            distillates=distillates,
        )


@app.route("/orders/<order_id>/close")
@login_required
def close_table(order_id):
    is_manager = check_role(role_hash("manager"), current_user.web3_address)
    is_waiter = check_role(role_hash("waiter"), current_user.web3_address)
    if is_manager or is_waiter:
        order = db.session.query(Order).filter_by(id=order_id).first()
        order.paid = True
        db.session.add(order)
        db.session.commit()
        flash("successfully closed table")
        return redirect(url_for("tables_management"))
    else:
        flash("Only managers and waiters can close a table")
        return redirect(url_for("dashboard"))
