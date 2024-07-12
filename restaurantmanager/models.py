from restaurantmanager import db
import enum


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
    main = 2
    dessert = 3
    pizza_topping = 4
    water = 5
    juice = 6
    soft_drinks = 7
    wine = 8
    beer = 9
    distillates = 10
    other = 11


class StockManagement(enum.Enum):
    # enum for the stock type
    preparation = 1
    wastage = 2


class OrderStatus(enum.Enum):
    # enum for the order status
    pending = 1
    accepted = 2
    delivered = 3
    cancelled = 4


boughtitem_manufactoreditem = db.Table(
    # table for the many to many relationship between boughtitems and manufactoreditems
    'boughtitem_manufactoreditem',
    db.Column('boughtitem_id', db.Integer, db.ForeignKey(
        'boughtitems.id', ondelete="CASCADE")),
    db.Column('manufactoreditem_id', db.Integer, db.ForeignKey(
        'manufactoreditems.id', ondelete="CASCADE"))
)

boughtitem_sellable_item = db.Table(
    # table for the many to many relationship between boughtitems and sellableitems
    'boughtitem_sellableitem',
    db.Column('boughtitem_id', db.Integer, db.ForeignKey(
        'boughtitems.id', ondelete="CASCADE")),
    db.Column('sellableitem_id', db.Integer, db.ForeignKey(
        'sellableitems.id', ondelete="CASCADE"))
)

manufactoreditem_sellableitem = db.Table(
    # table for the many to many relationship between manufactoreditems and sellableitems
    'manufactoreditem_sellableitem',
    db.Column('manufactoreditem_id', db.Integer, db.ForeignKey(
        'manufactoreditems.id', ondelete="CASCADE")),
    db.Column('sellableitem_id', db.Integer, db.ForeignKey(
        'sellableitems.id', ondelete="CASCADE"))
)

order_sellableitems = db.Table(
    # table for the many to many relationship between orders and sellableitems
    'order_sellableitems',
    db.Column('order_id', db.Integer, db.ForeignKey(
        'orders.id', ondelete="CASCADE")),
    db.Column('sellableitem_id', db.Integer, db.ForeignKey(
        'sellableitems.id', ondelete="CASCADE"))
)

delivery_boughtitems = db.Table(
    # table for the many to many relationship between deliveries and boughtitems
    'delivery_boughtitems',
    db.Column('delivery_id', db.Integer, db.ForeignKey(
        'deliveries.id', ondelete="CASCADE")),
    db.Column('boughtitem_id', db.Integer, db.ForeignKey(
        'boughtitems.id', ondelete="CASCADE"))
)

class User(db.Model):
    # schema for the user table
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    web3_address = db.Column(db.String(42), unique=True, nullable=False)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    f_name = db.Column(db.String(20), nullable=True)
    l_name = db.Column(db.String(20), nullable=True)
    google_id = db.Column(db.String, nullable=True)
    email = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    vat_number = db.Column(db.String, nullable=True)
    roles = db.Column(db.ARRAY(db.String), default = [])

    def __repr__(self):
        return "#{0} | {1} | Roles: {2}".format(self.id, self.web3_address, self.roles)


class Message(db.Model):
    # schema for the message table
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    board = db.Column(db.Enum(Board), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "#{0} | from {1} to {2} @ {3}".format(self.id, self.sender_id, self.board, self.timestamp)


class Wallet(db.Model):
    # schema for the wallet table
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey((
        'users.id'), ondelete="CASCADE"), nullable=False)
    mnemonic = db.Column(db.String, nullable=False)
    priv = db.Column(db.String, nullable=False)

    def  __repr__(self):
        return "#{0} - {1}".format(self.id, self.user_id)


class Supplier(db.Model):
    # schema for the supplier table
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    info = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "#{0} - Name: {1} | Phone {2}".format(self.id, self.name, self.phone)
    

class BoughtItem(db.Model):
    # schema for the boughtitem table
    __tablename__ = 'boughtitems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey(
        'suppliers.id', ondelete="CASCADE"), nullable=False)
    supplier_reference = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "#{0} | Name: {1} | Supplier id:{2} | Stock: {3}".format(self.id, self.name, self.supplier_id, self.stock)


class ManufactoredItem(db.Model):
    # schema for the dish table
    __tablename__ = 'manufactoreditems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    bought_items = db.relationship(
        'BoughtItem', secondary=boughtitem_manufactoreditem, primaryjoin=(boughtitem_manufactoreditem.c.boughtitem_id == id), secondaryjoin=(
            boughtitem_manufactoreditem.c.manufactoreditem_id == id), backref=db.backref("boughtitem_manufactoreditem", lazy=True), lazy=True)
    stock = db.Column(db.Integer, nullable=False)
    
    recipe = db.Column(db.Integer, db.ForeignKey(
        'recipes.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "#{0} | Name: {1} | Price: {2}".format(self.id, self.name, self.stock)


class Recipe(db.Model):
    # schema for the recipe table
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    ingredients = db.Column(db.ARRAY(db.Integer), default=[])
    quantities = db.Column(db.ARRAY(db.Integer), default=[])
    stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "#{0} | Yield: {1}".format(self.id, self.stock)


class SellableItem(db.Model):
    # schema for the sellableitem table
    __tablename__ = 'sellableitems'

    id = db.Column(db.Integer, primary_key=True)
    manufactured_items = db.relationship(
        "ManufactoredItem", secondary=manufactoreditem_sellableitem, primaryjoin=(manufactoreditem_sellableitem.c.manufactoreditem_id == id), secondaryjoin=(
            manufactoreditem_sellableitem.c.sellableitem_id == id), backref=db.backref("manufactoreditem_sellableitem", lazy=True), lazy=True)
    bought_items = db.relationship(
        "BoughtItem", secondary=boughtitem_sellable_item, primaryjoin=(boughtitem_sellable_item.c.boughtitem_id == id), secondaryjoin=(
            boughtitem_sellable_item.c.sellableitem_id == id), backref=db.backref("boughtitem_sellable_item", lazy=True), lazy=True)
    instock = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=True)
    kind = db.Column(db.Enum(ItemKind), nullable=False)

    def __repr__(self):
        return "#{0} | Name: {1} | Price: {2}".format(self.id, self.name, self.price)


class StockMovement(db.Model):
    # schema for the preparations table
    __tablename__ = 'stockmovements'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'boughtitems.id', ondelete="CASCADE"), nullable=False)
    item_kind = db.Column(db.Enum(ItemKind), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "#{0} | Preparation: {1} | Date: {2} | Quantity: {3}".format(self.id, self.date, self.quantity)


class Order(db.Model):
    # schema for orders table
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False)
    items = db.relationship("SellableItem", secondary=order_sellableitems, primaryjoin=(order_sellableitems.c.order_id == id), secondaryjoin=(
        order_sellableitems.c.sellableitem_id == id), backref=db.backref("order_sellableitems", lazy=True), lazy=True)
    supplier_reference = db.Column(db.String, nullable=False)
    table = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "#{0} | Date: {1} | Status: {2}".format(self.id, self.dateTime, self.status)


class Delivery(db.Model):
    # schema for supplier deliveries table
    __tablename__ = 'deliveries'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey(
        'suppliers.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    items = db.relationship("BoughtItem", secondary="delivery_boughtitems", primaryjoin=(delivery_boughtitems.c.delivery_id == id), secondaryjoin=(
        delivery_boughtitems.c.boughtitem_id == id), backref=db.backref("delivery_boughitems", lazy=True), lazy=True)
    supplier_reference = db.Column(db.String, nullable=False)
    info = db.Column(db.Text)

    def __repr__(self):
        return "#{0} | Date: {1}".format(self.supplier_id, self.date)