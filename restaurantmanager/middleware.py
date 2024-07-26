from flask import request
from restaurantmanager import db

from restaurantmanager.models import (
    Delivery,
    Ingredient,
    ManufactoredIngredient,
    PlacedOrder,
    Recipe,
    IngredientQuantity,
    ManufactoredIngredientQuantity,
    Supplier,
    recipe_ingredientquantity,
    recipe_manufactoredingredientquantity,
    placedorder_ingredientquantity,
    delivery_ingredientquantity,
    stockmovement_ingredientquantity,
    stockmovement_manufactoredingredientquantity,
    order_manufactoredingredientquantity,
)


def get_ingredient_quantity_from_form(keys,form):
    ingredient_quantities = []
    for key in keys:
        if (
            "ingredient_quantity" in key
            and "manufactored_ingredient_quantity" not in key
        ):
            ingredient_id = int(key.split("_")[-1])
            if form[key] != "" and form[key] != 0:
                quantity = int(form[key])
                ingredient_quantities.append(
                    {"ingredient_id": ingredient_id, "quantity": quantity}
                )
    return ingredient_quantities


def get_manufactored_ingredient_quantity_from_form(keys, form):
    ingredient_quantities = []
    for key in keys:
        if "manufactored_ingredient_quantity" in key:
            ingredient_id = int(key.split("_")[-1])
            if form[key] != "":
                quantity = int(form[key])
                ingredient_quantities.append(
                    {"manufactored_ingredient_id": ingredient_id, "quantity": quantity}
                )
    return ingredient_quantities


def append_ingredient_quantity(ingredient_quantities, table):
    for ingredient_quantity in ingredient_quantities:
        if ingredient_quantity['quantity'] != 0:
            new_ingredient_quantity = IngredientQuantity(
                ingredient_id=ingredient_quantity['ingredient_id'],
                quantity=ingredient_quantity['quantity'],
            )
            table.ingredient_quantities.append(new_ingredient_quantity)
    db.session.add(table)
    return True


def append_manufactored_ingredient_quantity(ingredient_quantities, table):
    for ingredient_quantity in ingredient_quantities:
        if ingredient_quantity['quantity'] != 0:
            new_manufactored_ingredient_quantity = ManufactoredIngredientQuantity(ingredient_id=ingredient_quantity['ingredient_id'], quantity=ingredient_quantity['quantity'])
            table.ingredient_quantities.append(new_manufactored_ingredient_quantity)
    db.session.add(table)
    return True


def update_ingredient_quantity(ingredient_quantities, table):
    table.ingredient_quantities.clear()
    db.session.add(table)
    db.session.commit()    
    assert append_ingredient_quantity(ingredient_quantities, table)
    return True


def increase_stock(ingredient_quantities):
    for ingredient_quantity in ingredient_quantities:
        ingredient = (
            db.session.query(Ingredient)
            .filter_by(id=ingredient_quantity['ingredient_id'])
            .first()
        )
        ingredient.stock_in_weight += ingredient_quantity['quantity']
        db.session.add(ingredient)
    return True


def decrease_stock(ingredient_quantities):
    for ingredient_quantity in ingredient_quantities:
        ingredient = (
            db.session.query(Ingredient)
            .filter_by(id=ingredient_quantity['ingredient_id'])
            .first()
        )
        ingredient.stock_in_weight -= ingredient_quantity['quantity']
    return True


