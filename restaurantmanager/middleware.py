import math
from flask import request
from restaurantmanager import db

from restaurantmanager.models import (
    Delivery,
    Ingredient,
    ManufactoredIngredient,
    Order,
    PlacedOrder,
    Recipe,
    IngredientQuantity,
    ManufactoredIngredientQuantity,
    StockManagement,
    StockMovement,
    Supplier,
    recipe_ingredientquantity,
    recipe_manufactoredingredientquantity,
    placedorder_ingredientquantity,
    delivery_ingredientquantity,
    stockmovement_ingredientquantity,
    stockmovement_manufactoredingredientquantity,
    order_manufactoredingredientquantity,
)


def get_ingredient_quantity_from_form(keys, form):
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
        if ingredient_quantity["quantity"] != 0:
            ingredientquantity = (
                db.session.query(IngredientQuantity)
                .filter_by(ingredient_id=ingredient_quantity["ingredient_id"])
                .filter_by(quantity=ingredient_quantity["quantity"])
                .first()
            )
            if ingredientquantity != None:
                table.ingredient_quantities.append(ingredientquantity)
            else:
                new_ingredient_quantity = IngredientQuantity(
                    ingredient_id=ingredient_quantity["ingredient_id"],
                    quantity=ingredient_quantity["quantity"],
                )
                db.session.add(new_ingredient_quantity)
                table.ingredient_quantities.append(new_ingredient_quantity) 
    db.session.add(table)
    db.session.commit()
    return True


def append_manufactored_ingredient_quantity(ingredient_quantities, table):
    for ingredient_quantity in ingredient_quantities:
        if ingredient_quantity["quantity"] != 0:
            manufactoredingredient_quantity = (
                db.session.query(ManufactoredIngredientQuantity)
                .filter_by(
                    manufactored_ingredient_id=ingredient_quantity[
                        "manufactored_ingredient_id"
                    ]
                )
                .filter_by(quantity=ingredient_quantity["quantity"])
                .first()
            )
            if manufactoredingredient_quantity != None:
                table.manufactoredingredient_quantities.append(
                    manufactoredingredient_quantity
                )

            else:
                new_manufactored_ingredient_quantity = ManufactoredIngredientQuantity(
                    manufactored_ingredient_id=ingredient_quantity[
                        "manufactored_ingredient_id"
                    ],
                    quantity=ingredient_quantity["quantity"],
                )
                db.session.add(new_manufactored_ingredient_quantity)
                table.manufactoredingredient_quantities.append(
                    new_manufactored_ingredient_quantity
                )
    db.session.add(table)
    db.session.commit()
    return True


def update_ingredient_quantity(ingredient_quantities, table):
    table.ingredient_quantities.clear()
    db.session.add(table)
    db.session.commit()
    assert append_ingredient_quantity(ingredient_quantities, table)
    return True


def update_manufactored_ingredient_quantity(ingredient_quantities, table):
    table.manufactoredingredient_quantities.clear()
    db.session.add(table)
    db.session.commit()
    assert append_manufactored_ingredient_quantity(ingredient_quantities, table)
    return True


def increase_stock(ingredient_quantities):
    for ingredient_quantity in ingredient_quantities:
        ingredient = (
            db.session.query(Ingredient)
            .filter_by(id=ingredient_quantity["ingredient_id"])
            .first()
        )
        ingredient.stock_in_weight += ingredient_quantity["quantity"]
        db.session.add(ingredient)
    return True


def decrease_stock(ingredient_quantities):
    for ingredient_quantity in ingredient_quantities:
        ingredient = (
            db.session.query(Ingredient)
            .filter_by(id=ingredient_quantity["ingredient_id"])
            .first()
        )
        ingredient.stock_in_weight -= ingredient_quantity["quantity"]
    return True


def increase_stock_manufactored(ingredient_quantities):
    for ingredient_quantity in ingredient_quantities:
        ingredient = (
            db.session.query(ManufactoredIngredient)
            .filter_by(id=ingredient_quantity["manufactored_ingredient_id"])
            .first()
        )
        ingredient.stock_in_portions += int(ingredient_quantity["quantity"])
        db.session.add(ingredient)
    return True


def decrease_stock_manufactored(ingredient_quantities):
    for ingredient_quantity in ingredient_quantities:
        ingredient = (
            db.session.query(ManufactoredIngredient)
            .filter_by(id=ingredient_quantity["manufactored_ingredient_id"])
            .first()
        )
        ingredient.stock_in_portions -= int(ingredient_quantity["quantity"])
        db.session.add(ingredient)
    return True


def get_ingredient_related_recipes(related_recipe_ids):
    related_recipes_data = []
    for related_recipe_id in related_recipe_ids:
        related_recipes = db.session.query(Recipe).filter_by(id=related_recipe_id).all()
        for related_recipe in related_recipes:
            recipe = db.session.query(Recipe).filter_by(id=related_recipe.id).first()
            item = (
                db.session.query(ManufactoredIngredient)
                .filter_by(id=recipe.recipe_for)
                .first()
            )
            related_recipes_data.append(
                {
                    "id": recipe.id,
                    "name": item.name,
                    "description": item.description,
                    "sellable": item.sellable_item,
                }
            )
    return related_recipes_data


def get_ingredient_related_placedorders(related_placedorder_ids):
    related_placedorder_data = []
    for related_placedorder_id in related_placedorder_ids:
        related_placedorder = (
            db.session.query(PlacedOrder).filter_by(id=related_placedorder_id).first()
        )
        supplier = (
            db.session.query(Supplier)
            .filter_by(id=related_placedorder.supplier_id)
            .first()
        )
        related_ingredient_quantity = (
            db.session.query(placedorder_ingredientquantity)
            .filter_by(placedorder_id=related_placedorder.id)
            .first()
        )
        ingredient_quantity = (
            db.session.query(IngredientQuantity)
            .filter_by(id=related_ingredient_quantity.ingredient_quantity_id)
            .first()
        )
        related_placedorder_data.append(
            {
                "id": related_placedorder.id,
                "date": related_placedorder.dateTime,
                "supplier": supplier.name,
                "supplier_id": supplier.id,
                "quantity": ingredient_quantity.quantity,
            }
        )
    return related_placedorder_data


def get_ingredient_related_deliveries(related_delivery_ids):
    related_delivery_data = []
    for related_delivery_id in related_delivery_ids:
        related_delivery = (
            db.session.query(Delivery).filter_by(id=related_delivery_id).first()
        )
        supplier = (
            db.session.query(Supplier)
            .filter_by(id=related_delivery.supplier_id)
            .first()
        )
        related_ingredient_quantity = (
            db.session.query(delivery_ingredientquantity)
            .filter_by(delivery_id=related_delivery.id)
            .first()
        )
        ingredient_quantity = (
            db.session.query(IngredientQuantity)
            .filter_by(id=related_ingredient_quantity.ingredient_quantity_id)
            .first()
        )
        related_delivery_data.append(
            {
                "id": related_delivery.id,
                "date": related_delivery.date,
                "delivery_info": related_delivery.info,
                "supplier": supplier.name,
                "supplier_id": supplier.id,
                "quantity": ingredient_quantity.quantity,
            }
        )
    return related_delivery_data


def get_ingredient_related_stockmovements(related_stockmovement_ids):
    wastages = []
    preparations = []
    stock_takes = []
    for related_stockmovement_id in related_stockmovement_ids:
        related_stockmovement = (
            db.session.query(StockMovement)
            .filter_by(id=related_stockmovement_id)
            .first()
        )
        related_ingredient_quantity = (
            db.session.query(stockmovement_ingredientquantity)
            .filter_by(stockmovement_id=related_stockmovement.id)
            .first()
        )
        ingredient_quantity = (
            db.session.query(IngredientQuantity)
            .filter_by(id=related_ingredient_quantity.ingredient_quantity_id)
            .first()
        )
        if related_stockmovement.preparation_kind == StockManagement(2):
            wastages.append(
                {
                    "id": related_stockmovement.id,
                    "date": related_stockmovement.date,
                    "stockmovement_info": related_stockmovement.info,
                    "quantity": ingredient_quantity.quantity,
                }
            )
        elif related_stockmovement.preparation_kind == StockManagement(1):
            preparations.append(
                {
                    "id": related_stockmovement.id,
                    "date": related_stockmovement.date,
                    "quantity": ingredient_quantity.quantity,
                }
            )
        elif related_stockmovement.preparation_kind == StockManagement(3):
            stock_takes.append(
                {
                    "id": related_stockmovement.id,
                    "date": related_stockmovement.date,
                    "quantity": ingredient_quantity.quantity,
                }
            )
    return wastages, preparations, stock_takes


def get_manufactored_ingredient_related_stockmovements(related_stockmovement_ids):
    wastages = []
    preparations = []
    stock_takes = []
    for related_stockmovement_id in related_stockmovement_ids:
        related_stockmovement = (
            db.session.query(StockMovement)
            .filter_by(id=related_stockmovement_id)
            .first()
        )
        related_ingredient_quantity = (
            db.session.query(stockmovement_manufactoredingredientquantity)
            .filter_by(stockmovement_id=related_stockmovement.id)
            .first()
        )
        ingredient_quantity = (
            db.session.query(ManufactoredIngredientQuantity)
            .filter_by(
                id=related_ingredient_quantity.manufactoredingredient_quantity_id
            )
            .first()
        )
        if related_stockmovement.preparation_kind == StockManagement(2):
            wastages.append(
                {
                    "id": related_stockmovement.id,
                    "date": related_stockmovement.date,
                    "stockmovement_info": related_stockmovement.info,
                    "quantity": ingredient_quantity.quantity,
                }
            )
        elif related_stockmovement.preparation_kind == StockManagement(1):
            preparations.append(
                {
                    "id": related_stockmovement.id,
                    "date": related_stockmovement.date,
                    "quantity": ingredient_quantity.quantity,
                }
            )
        elif related_stockmovement.preparation_kind == StockManagement(3):
            stock_takes.append(
                {
                    "id": related_stockmovement.id,
                    "date": related_stockmovement.date,
                    "quantity": ingredient_quantity.quantity,
                }
            )
    return wastages, preparations, stock_takes


def get_manufactored_ingredient_related_orders(related_order_ids):
    related_order_data = []
    for related_order_id in related_order_ids:
        related_order = db.session.query(Order).filter_by(id=related_order_id).first()
        related_ingredient_quantity = (
            db.session.query(stockmovement_manufactoredingredientquantity)
            .filter_by(stockmovement_id=related_order.id)
            .first()
        )
        ingredient_quantity = (
            db.session.query(ManufactoredIngredientQuantity)
            .filter_by(
                id=related_ingredient_quantity.manufactoredingredient_quantity_id
            )
            .first()
        )
        related_order_data.append(
            {
                "id": related_order.id,
                "date": related_order.dateTime,
                "table": related_order.table,
                "quantity": ingredient_quantity.quantity,
            }
        )
    return related_order_data


def get_manufactored_ingredient_related_recipes(related_recipe_ids):
    related_recipes_data = []
    for related_recipe_id in related_recipe_ids:
        related_recipes = db.session.query(Recipe).filter_by(id=related_recipe_id).all()
        for related_recipe in related_recipes:
            recipe = db.session.query(Recipe).filter_by(id=related_recipe.id).first()
            item = (
                db.session.query(ManufactoredIngredient)
                .filter_by(id=recipe.recipe_for)
                .first()
            )
            related_recipes_data.append(
                {
                    "id": recipe.id,
                    "name": item.name,
                    "description": item.description,
                    "sellable": item.sellable_item,
                }
            )
    return related_recipes_data


def calculate_preparation_quantities(recipe, portions):
    ingredient_quantities = []
    manufactored_ingredient_quantities = []
    for ingredient_quantity in recipe.ingredient_quantities:
        quantity_used = math.floor(
            int(portions) * int(ingredient_quantity.quantity) / int(recipe.portions)
        )
        ingredient_quantities.append(
            {
                "ingredient_id": ingredient_quantity.ingredient_id,
                "quantity": quantity_used,
            }
        )
    for manufactored_ingredient_quantity in recipe.manufactoredingredient_quantities:
        quantity_used = math.floor(
            int(portions)
            * int(manufactored_ingredient_quantity.quantity)
            / int(recipe.portions)
        )
        manufactored_ingredient_quantities.append(
            {
                "ingredient_id": manufactored_ingredient_quantity.ingredient_id,
                "quantity": quantity_used,
            }
        )
    return ingredient_quantities, manufactored_ingredient_quantities
