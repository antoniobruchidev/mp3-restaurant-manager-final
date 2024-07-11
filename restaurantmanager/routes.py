from flask import render_template
from restaurantmanager import app, db
from restaurantmanager.models import Message, User, Wallet, Supplier, BoughtItem, ManufactoredItem, Recipe, SellableItem, StockMovement, Order, Delivery


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')