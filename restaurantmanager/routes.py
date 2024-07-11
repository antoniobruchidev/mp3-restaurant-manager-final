from flask import render_template
from restaurantmanager import app, db

@app.route('/')
def home():
    return render_template('base.html')