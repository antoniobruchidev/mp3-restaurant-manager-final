from flask import request
from restaurantmanager import db

from restaurantmanager.models import Ingredient, IngredientQuantity, ManufactoredIngredientQuantity


def get_ingredient_quantity(keys):
    ingredient_quantities = []
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
                ingredient_quantities.append(item_quantity)
    return ingredient_quantities


def get_manufactored_ingredient_quantity(keys):
    ingredient_quantities = []
    for key in keys:
        if "manufactored_ingredient_quantity" in key:
            ingredient_id = int(key.split("_")[-1])
            if request.form[key] != "":
                quantity = int(request.form[key])
                item_quantity_query = (
                    db.session.query(ManufactoredIngredientQuantity)
                    .filter_by(manufactored_ingredient_id = ingredient_id)
                    .filter_by(quantity = quantity)
                    .first()
                )
                if item_quantity_query:
                    item_quantity = item_quantity_query
                else:
                    item_quantity = ManufactoredIngredientQuantity(
                        manufactored_ingredient_id=ingredient_id, quantity=quantity
                    )
                ingredient_quantities.append(item_quantity)       
    return ingredient_quantities


def append_ingredient_quantity(ingredient_quantities, table):
    for ingredient_quantity in ingredient_quantities:
        db.session.add(ingredient_quantity)
        table.ingredient_quantities.append(ingredient_quantity)
    return True


def append_manufactored_ingredient_quantity(ingredient_quantities, table):
    for ingredient_quantity in ingredient_quantities:
        db.session.add(ingredient_quantity)
        table.manufactoredingredient_quantities.append(ingredient_quantity)
    return True


def increase_stock(ingredient_quantities):
    for ingredient_quantity in ingredient_quantities:
        ingredient = db.session.query(Ingredient).filter_by(id=ingredient_quantity.ingredient_id).first()
        ingredient.stock_in_weight += ingredient_quantity.quantity
    return True


def decrease_stock(ingredient_quantities):
    for ingredient_quantity in ingredient_quantities:
        ingredient = db.session.query(Ingredient).filter_by(id=ingredient_quantity.ingredient_id).first()
        ingredient.stock_in_weight -= ingredient_quantity.quantity
    return True
