from restaurantmanager import db
import enum
from flask_login import UserMixin


class AccountType(enum.Enum):
    # enum for the account type
    web3_eoa = 1
    email_eoa = 2
    google = 3


class Board(enum.Enum):
    # enum for the messageboard
    owner = 1
    manager = 2
    chef = 3
    waiter = 4
    public = 5


class ItemKind(enum.Enum):
    # enum for the dish type
    starter = 1
    pasta = 2
    pizza = 3
    main = 4
    dessert = 5
    pizza_topping = 6
    water = 7
    juice = 8
    soft_drinks = 9
    wine = 10
    beer = 11
    distillates = 12
    other = 13


class StockManagement(enum.Enum):
    # enum for the stock type
    preparation = 1
    wastage = 2
    stock_take = 3


class OrderStatus(enum.Enum):
    # enum for the order status
    pending = 1
    accepted = 2
    delivered = 3
    cancelled = 4


recipe_ingredientquantity = db.Table(
    # table for the many to many relationship between recipes and manufactored ingredients
    "recipe_ingredientquantities",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE")),
    db.Column(
        "ingredient_quantity_id",
        db.Integer,
        db.ForeignKey("ingredientquantities.id", ondelete="CASCADE"),
    ),
)

recipe_manufactoredingredientquantity = db.Table(
    # table for the many to many relationship between recipes and manufactored ingredients
    "recipe_manufactoredingredientquantities",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE")),
    db.Column(
        "manufactoredingredient_quantity_id",
        db.Integer,
        db.ForeignKey("manufactoredingredientquantities.id", ondelete="CASCADE"),
    ),
)

stockmovement_ingredientquantity = db.Table(
    # table for the many to many relationship between stock movements and manufactored ingredients
    "stockmovement_ingredientquantities",
    db.Column(
        "stockmovement_id",
        db.Integer,
        db.ForeignKey("stockmovements.id", ondelete="CASCADE"),
    ),
    db.Column(
        "ingredient_quantity_id",
        db.Integer,
        db.ForeignKey("ingredientquantities.id", ondelete="CASCADE"),
    ),
)

stockmovement_manufactoredingredientquantity = db.Table(
    # table for the many to many relationship between stock movements and manufactored ingredients
    "stockmovement_manufactorediingredientquantities",
    db.Column(
        "stockmovement_id",
        db.Integer,
        db.ForeignKey("stockmovements.id", ondelete="CASCADE"),
    ),
    db.Column(
        "manufactoredingredient_quantity_id",
        db.Integer,
        db.ForeignKey("manufactoredingredientquantities.id", ondelete="CASCADE"),
    ),
)

order_manufactoredingredientquantity = db.Table(
    # table for the many to many relationship between orders and manufactored ingredients quantities
    "order_manufactoredingredientquantities",
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE")),
    db.Column(
        "manufactoredingredient_quantity_id",
        db.Integer,
        db.ForeignKey("manufactoredingredientquantities.id", ondelete="CASCADE"),
    ),
)

placedorder_ingredientquantity = db.Table(
    # table for the many to many relationship between order placed and ingredient quantities
    "placedorder_ingredientquantities",
    db.Column(
        "placedorder_id",
        db.Integer,
        db.ForeignKey("placedorders.id", ondelete="CASCADE"),
    ),
    db.Column(
        "ingredient_quantity_id",
        db.Integer,
        db.ForeignKey("ingredientquantities.id", ondelete="CASCADE"),
    ),
)

delivery_ingredientquantity = db.Table(
    # table for the many to many relationship between deliveries and ingredient quantities
    "delivery_ingredientquantities",
    db.Column(
        "delivery_id", db.Integer, db.ForeignKey("deliveries.id", ondelete="CASCADE")
    ),
    db.Column(
        "ingredient_quantity_id",
        db.Integer,
        db.ForeignKey("ingredientquantities.id", ondelete="CASCADE"),
    ),
)


class User(db.Model, UserMixin):
    # schema for the user table
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    web3_address = db.Column(db.String(42), unique=True, nullable=False)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    f_name = db.Column(db.String(20), nullable=True)
    l_name = db.Column(db.String(20), nullable=True)
    google_id = db.Column(db.String, nullable=True)
    email = db.Column(db.String(66), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    vat_number = db.Column(db.String, nullable=True)
    roles = db.Column(db.Boolean, default=False)
    activated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "#{0} | {1} | Roles: {2}".format(self.id, self.web3_address, self.roles)


class BoardMessage(db.Model):
    # schema for the message table
    __tablename__ = "boardmessages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    board = db.Column(db.Enum(Board), nullable=False)
    subject = db.Column(db.String, nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    replies = db.relationship("BoardMessageReply", backref="boardmessages")

    def __repr__(self):
        return "#{0} | Board: {2} from {1} @ {3}".format(
            self.id, self.sender_id, self.board, self.timestamp
        )


class BoardMessageReply(db.Model):
    # schema for message replies table
    __tablename__ = "boardmessagereplies"
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(
        db.Integer,
        db.ForeignKey("boardmessages.id", ondelete="CASCADE"),
        nullable=False,
    )
    reply = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "#{0} | Reply: {2} to {1} @ {3}".format(
            self.id, self.message_id, self.reply, self.timestamp
        )


class InternalMessage(db.Model):
    # schema for the mail table
    __tablename__ = "internalmessages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    recipient_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "#{0} | From: {1} To: {2} Subject:{3} @ {4}".format(
            self.id, self.sender_id, self.recipient_id, self.subject, self.timestamp
        )


class Wallet(db.Model):
    # schema for the wallet table
    __tablename__ = "wallets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(("users.id"), ondelete="CASCADE"), nullable=False
    )
    mnemonic = db.Column(db.String, nullable=False)
    priv = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "#{0} - {1}".format(self.id, self.user_id)


class Supplier(db.Model):
    # schema for the supplier table
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    info = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "#{0} - Name: {1} | Phone {2}".format(self.id, self.name, self.phone)


class Ingredient(db.Model):
    # schema for the ingredient table
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    supplier_id = db.Column(
        db.Integer, db.ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False
    )
    supplier_reference = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    stock_in_weight = db.Column(db.Integer, default=0)
    allergens = db.Column(db.ARRAY(db.String), default=[])

    def __repr__(self):
        return "#{0} | Name: {1} | Supplier id:{2} | Stock: {3} grams".format(
            self.id, self.name, self.supplier_id, self.stock_in_weight
        )


class ManufactoredIngredient(db.Model):
    # schema for the manufactored ingredient table
    __tablename__ = "manufactoredingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    stock_in_portions = db.Column(db.Integer, default=0)
    sellable_item = db.Column(db.Boolean, default=False)
    kind = db.Column(db.Enum(ItemKind), default=ItemKind(12))
    price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return "#{0} | Name: {1} | Stock: {2} portions".format(
            self.id, self.name, self.stock_in_portions
        )


class IngredientQuantity(db.Model):
    # schema for the ingredient quantites table
    __tablename__ = "ingredientquantities"

    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredients.id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "#{0} - {1} grams".format(self.ingredient_id, self.quantity)


class ManufactoredIngredientQuantity(db.Model):
    # schema for the manufactored ingredient quantites table
    __tablename__ = "manufactoredingredientquantities"

    id = db.Column(db.Integer, primary_key=True)
    manufactored_ingredient_id = db.Column(
        db.Integer, db.ForeignKey("manufactoredingredients.id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "#{0} - {1} portions".format(
            self.manufactored_ingredient_id, self.quantity
        )


class Recipe(db.Model):
    # schema for the recipe table
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    recipe_for = db.Column(
        db.Integer, db.ForeignKey("manufactoredingredients.id"), nullable=False
    )
    ingredient_quantities = db.relationship(
        "IngredientQuantity", secondary=recipe_ingredientquantity, backref="recipes", lazy=True
    )
    manufactoredingredient_quantities = db.relationship(
        "ManufactoredIngredientQuantity",
        secondary=recipe_manufactoredingredientquantity,
        backref="recipes",
        lazy=True,
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    portions = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "#{0} | Yield: {1}".format(self.id, self.portions)


class StockMovement(db.Model):
    # schema for the preparations table
    __tablename__ = "stockmovements"

    id = db.Column(db.Integer, primary_key=True)
    ingredient_quantities = db.relationship(
        "IngredientQuantity",
        secondary=stockmovement_ingredientquantity,
        backref="stockmovements",
        lazy=True,
    )
    manufactoredingredient_quantities = db.relationship(
        "ManufactoredIngredientQuantity",
        secondary=stockmovement_manufactoredingredientquantity,
        backref="stockmovements",
        lazy=True,
    )
    preparation_kind = db.Column(db.Enum(StockManagement), nullable=False)
    info = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    employee_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return "#{0} | Preparation: {1} | Date: {2}".format(
            self.id, self.date, self.preparation_kind
        )


class Order(db.Model):
    # schema for orders table
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    dateTime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False)
    manufactoredimgredient_quantities = db.relationship(
        "ManufactoredIngredientQuantity",
        secondary=order_manufactoredingredientquantity,
        backref="orders",
        lazy=True,
    )
    supplier_reference = db.Column(db.String, nullable=False)
    table = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "#{0} | Date: {1} | Status: {2}".format(
            self.id, self.dateTime, self.status
        )


class PlacedOrder(db.Model):
    # schema for placed orders table
    __tablename__ = "placedorders"
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime, nullable=False)
    ingredient_quantities = db.relationship(
        "IngredientQuantity",
        secondary=placedorder_ingredientquantity,
        backref="placedorders",
        lazy=True,
    )
    sent = db.Column(db.Boolean, default=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)


class Delivery(db.Model):
    # schema for supplier deliveries table
    __tablename__ = "deliveries"

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(
        db.Integer, db.ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    date = db.Column(db.DateTime, nullable=False)
    ingredient_quantities = db.relationship(
        "IngredientQuantity",
        secondary=delivery_ingredientquantity,
        backref="deliveries",
        lazy=True,
    )
    supplier_reference = db.Column(db.String, nullable=False)
    info = db.Column(db.Text)

    def __repr__(self):
        return "#{0} | Date: {1}".format(self.supplier_id, self.date)
