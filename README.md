# Carpez Kitchen Manager
A platform for managing kitchens. 

## UX
The platform targets any company in the hospitality industry. The application is designed to distinguish its users in:
- UNREGISTERED USERS: Customers that are not registered with the company. They will be able to place orders when seated at the table once seated.
- USERS: Costumers that will register with the company. Via the platform they will be able to access their invoices (if they have any) and previous orders. Place orders at the table once they are seated.
- WAITERS: Company employees responsibile for taking and delivering orders. They will also be able to access stock take and deliveries for the beverages department.
- CHEFS: Company employees responsible for adding recipes for the menu dishes. They will also be able to access stock take and food for the beverages department and update the stock via preparation and wastage reports.
- MANAGERS: Company employees responsible for hiring and firing CHEFS and WAITERS. They will also be able to access stock take and food for the beverages departments. Everything above besides CHEFS preparations.
- OWNERS: Company partner that will be able to hire and fire MANAGERS CHEFS and WAITERS. Everything above besides CHEFS preparations.

The platform will be designed to use preparation and deliveries record to increse the inventory and wastage and orders to reduce it. It will also track the company's sales and showcase which dishes are the most popular.

### User Stories
- As an UNREGISTERED USER, I want the platform to be intuitive.
- As an UNREGISTERED USER, I want to be able to view the menu.
- As an UNREGISTERED USER, I want to be able to know the ingredients of the dishes.
- As an UNREGISTERED USER, I want to be able to place an order.
- As an UNREGISTERED USER, I want to be able to update or delete an order.
- As an USER, I want to be able to do everything a not registered user can.
- As an USER, I want to be able to view my invoice.
- As an USER, I want to be able to view my previous orders.
- As an USER, I want to be able to pay for my order.
- As an EMPLOYEE(WAITER, CHEF and MANAGER), I want the platform to be easy of use.
- As an OWNER, I want the platform to integrate Web3 and blockchain technology, at least for authentication process. Accepting payments would be optimal.
- As another OWNER, I'm afraid of technology and I want to have nothing to do with new stuff, every platform feature MUST also work without any additional extension.

### Strategy
The goal of this project is to create a platform that interacts with users and employees letting them access a variety of CRUD operations depending on their role.

### Scope
The platform is designed to be a restaurant management system. It will be able to:
- Hire and fire employees.
- Add and manage suppliers and their items.
- Keep track of deliveries and stock levels.
- Add recipes for a manufactored item or a dish.
- Keep track of preparations and wastages and automatically adjust stock levels.
- Show a menu with what is available.
- Add and manage orders.
- Keep track of sales and automatically adjust stock levels.
- Show data for preparations wastages and sales to improve efficiency.
- Register and login customers.
- Let registered customers see their previous orders and their invoices.

## Techologies
1. python 3.10.12
3. Flask-SQLAlchemy
4. HTML
5. CSS
6. JS
7. Materialize
8. Postgresql
9. Flask_Login
10. wtforms
11. Flask_Mail
12. web3

## Development

### User Authentication

Probably the trickiest part of this project given the owner's user stories.
I created an authentication process that can login users and employees, they can regiter and login the platform using Metamask or compatible ethereum wallet. They can also register and login with Google or simply using their email and a password.

#### The user register with metamask or compatible ethereum wallet.

The platform will store the user web3, address given and family name (not required), it will create a fake email in the form of web3_address@internal.kitchenmanager to populate the required email field. it will also create a password to populate the required password field, but the user will not be able to access the platform with the fake email and password until they change it after logging in with metamask. (To be implemented). The user won't need activation.

#### The user register with google

The platform will store the user google id, its email, given and family name. It will create a new ethereum wallet which will be assigned to the user, storing also the mnemonic phrase and private key (they should both be encrypted). It will also populate the password field with a password that the user won't be able to access the platform with until they change it after logging in with google.(To be implemented). The user won't need activation, maybe a simple confirmation email.

#### The user register with email and password

The platform will store the user email, given and family name (not required). It will create a new ethereum wallet which will be assigned to the user, storing also the mnemonic phrase and private key  (they should both be encrypted). It will also populate the password field with a password that the user won't be able to access the platform with until they change it after logging in with email and password.(To be implemented). The platform will send an email asking for the user to activate their account.

#### User login

Selecting metamask, or selecting google and clicking on the login button and selecting the desired google account will log the user in, if registered, redirecting to the dashboard.
Selecting email and password will log the user in, if registered and activated, redirecting to the dashboard.
With bad credentials the user will be redirected to the login page in any case. (To be implemented error message).

#### User registration validation

```python
restaurantmanager/forms.py (25-40)

    def validate_web3_address(self, web3_address):
        existing_web3_address = db.session.query(User).filter_by(
            web3_address=web3_address.data).first()
        if existing_web3_address:
            raise ValidationError('The web3 address is already in use')
        
    def validate_email(self, email):
        existing_email = db.session.query(User).filter_by(
            email=email.data).first()
        if existing_email:
            raise ValidationError('The email is already in use')
        
    def validate_account_type(self, account_type):
        if account_type.data == '0':
            raise ValidationError('Please choose an account type')
```

The above code ensure that user MUST select an account type and both web3 address and emails are uniques.

### Bugs and fixes

#### Many to many relationship, models refactoring and variables renaming - Commits: [1](https://github.com/antoniobruchidev/mp3-restaurant-manager/commit/2a6628f7f5289c6a698a865397ce08fbb29a44fd){:target="_blank"} - [2](https://github.com/antoniobruchidev/mp3-restaurant-manager/commit/7de505f8732f3821e17aff43255cfd0476d2bf0f){:target="_blank"} - [3](https://github.com/antoniobruchidev/mp3-restaurant-manager/commit/420544fbf48e273a405fa361fc595d376d1adcd1){:target="_blank"}

Once I started coding the part relevant to the creation of a new recipes, I realized my many to many relationships were poorly designed to work with my models. I had the SellableItem model relating to both BoughtItem and ManufactoredItem models, while I was trying to relate the quantities of the ingredients in the recipes storing them in unrelated array of integers inside the Recipe model. Like I said, poorly designed... I also had to fix some minor issues around in the models so it looked like a good moment to do some refactoring.
On top of it, looking around the web, I found [this](https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-sqlalchemy){:target="_blank"}, compared the defined relationships in those models and mines and it looked like my relationships were completely different, I honestly don't remember where I read about the previous code, but anyway after testing the new code, it was working fine so I decided to keep it.
Back to my models, I decided to create two new models, IngredientQuantity and ManufactoredIngredientQuantity, so I could relate them with every other table that require a quantity, from placed orders and deliveries and wastages of Ingredients to the sale, preparation or wastage of one or more ManufactoredIngredients (as long has they are flagged as sellable and their price is set).
Once I was at it I decided to rename some variables in a more semantic way and to add two new columns in the BoardMessage model for the message's subject and its replies.