# Carpez Kitchen Manager
A platform for managing kitchens.

## Live demo at [Carpez Kitchen Manager](https://carpez-kitchen-manager-e9e93ef660cf.herokuapp.com/)

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
- As an USER, I want the platform to be intuitive.
- As an EMPLOYEE(WAITER, CHEF and MANAGER), I want the platform to be easy of use.
- As a MANAGER, I want to be able to hire and fire CHEFS and WAITERS.
- As a Manager, I wawnt to be able to add suppliers and ingredients.
- As a MANAGER, I want to keep track of stock levels.
- As a Manager, I want to be able to place orders.
- As a Manager, I want to be able to add items to the order but send it later.
- As a MANAGER, I want to be able to track deliveries and their related info.
- As a MANAGER, I want CHEFS and WAITERS to be able to do wastage reports and add deliveries.
- As a CHEF, I want to be able to create recipes with the ingredients at hand.
- As a CHEF, I want to be able to change my recipes.
- As a MANAGER, I want to be able to price the recipe that will go in the menu.
- As a CHEF, I want to be able to prepare the recipes (for future revisions it'd be nice a labeling system for the manufactured ingredients).
- As a MANAGER, I want the platform to increase and decrease stock levels depending on wastage reports, sales, deliveries and preparations.
- As a MANAGER, I want to be able to manually reset the stock level as in a stock take.
- As an OWNER, I want the platform to integrate Web3 and blockchain technology, at least for authentication process. Accepting payments would be optimal.

### Strategy
The goal of this project is to create a platform that interacts with users and employees letting them access a variety of CRUD operations depending on their role.

### Scope
The platform is designed to be a restaurant stock management system. It will be able to:
- Hire and fire employees.
- Add and manage suppliers and their items.
- Keep track of deliveries and stock levels.
- Add recipes for a manufactored item or a dish.
- Keep track of preparations and wastages and automatically adjust stock levels.
- Show a menu with what is available.
- Add and manage orders.
- Keep track of sales and automatically adjust stock levels.
- Show data for preparations, wastages and sales to improve efficiency.
- Register and login customers.

### Structure
The platform is designed to be a web application. It is built using Flask and Flask-SQLAlchemy.

#### database diagram
![database diagram](

### Skeleton
The platform it's not as easy to use as it probably should be, but it's a good start. From the manage pagem the manager can search an ingredient in the searchbar and it will populate the collections in the materilize tabs. From there the manager can update the stock level or add the item to an open order from its supplier, or go the the recipe page of a manufactored item searched and maybe enabling a new dish in the menu by flagging the sellable item and giving it a price.
Chefs mostly live in the kitchen so they'll have access to wastage reports and the recipes pages, including editing the ingredients in a very easy way.

### Surface
The platform will be accessible by any device, including mobile devices. To access from mobile with web3 application the user needs to have Metamask installed.
We have the landing page which is the menu, populated with the dishes available at the moment.
From the navigation bar at the top, the user can login, or redirect to register from the login page, once logged the user will be presented with his dashboard, containing the user's messages and their answers. From their dashboard the user can access the previusly mentioned messageboard, in which, in real life situation, he'd probably find some notes and to dos.
Depending on their role the pages thhe user can access are different, or in a different way.

### MVP
- Create a a platform capable of running daily or so tasks and relate everything to the user in a dynamic way, menu included.
- Employees and registered users can leave messages on dedicated messageboards for manager, chefs and waiters. That is an important feature of the platform, as if an User has a dietary requirement, he can leave a message on the chefs messageboard and both the manager and the chef will be notified, if a User wants needs special accomodations from front of the house, space for wheelchairs, or lots of baby seats, they can leave it on the waiter messageboard and both waiters and managers will be notified.
- For a special customer experience the restaurant is intented to give a nice a la carte experience, with the meals varying a lot compared to a normal restaurant. This would slowly build up important losses from missed profits due too much wastage. From this the necessity to keep track of wastages and stock levels.
- For future editions it would be nice to add comment and stars to the menu containing user's feedback to our offer.
- Also for future editions, it would be very helpful to add a labeling system, to print labels for the items to store and table for storing due diligence data, including staff training, cleaning and temperature levels.

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

I created an authentication process that can login users and employees, they can register and login the platform using Metamask or compatible ethereum wallet. They can also register and login with Google or simply using their email and a password.

#### The user register with metamask or compatible ethereum wallet.

The platform will store the user web3, address given and family name (not required), it will create a fake email in the form of web3_address@internal.kitchenmanager to populate the required email field. it will also create a password to populate the required password field, but the user will not be able to access the platform with the fake email and password until they change it after logging in with metamask. (To be implemented). The user won't need activation.

#### The user register with google

The platform will store the user google id, its email, given and family name. It will create a new ethereum wallet which will be assigned to the user, storing also the mnemonic phrase and private key (they should both be encrypted). It will also populate the password field with a password that the user won't be able to access the platform with until they change it after logging in with google.(To be implemented). The user won't need activation, maybe a simple confirmation email.

#### The user register with email and password

The platform will store the user email, given and family name (not required). It will create a new ethereum wallet which will be assigned to the user, storing also the mnemonic phrase and private key  (they should both be encrypted). The platform will send an email asking for the user to activate their account. The user won't be able to access the platform until they activate the account.

#### User login

Clicking on metamask picture google icon will log the user in, if registered, redirecting to the dashboard.
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

#### Create Recipe Form

Since I didn't use wtforms like for the other endpoints, I decided to provide a reason. I had to create a form which inputs varies every time a new recipe is created. I honestly don't know if it is possible to define a dynamic form but it was not the time to look for it, honestly faster to create the form in html inside jinja templates and have javascript handle the form submission and redirection if successful.

### Bugs and fixes

#### Many to many relationship, models refactoring and variables renaming - Commits: [1](https://github.com/antoniobruchidev/mp3-restaurant-manager/commit/2a6628f7f5289c6a698a865397ce08fbb29a44fd){:target="_blank"} - [2](https://github.com/antoniobruchidev/mp3-restaurant-manager/commit/7de505f8732f3821e17aff43255cfd0476d2bf0f){:target="_blank"} - [3](https://github.com/antoniobruchidev/mp3-restaurant-manager/commit/420544fbf48e273a405fa361fc595d376d1adcd1){:target="_blank"}

Once I started coding the part relevant to the creation of a new recipes, I realized my many to many relationships were poorly designed to work with my models. I had the SellableItem model relating to both BoughtItem and ManufactoredItem models, while I was trying to relate the quantities of the ingredients in the recipes storing them in unrelated array of integers inside the Recipe model. Like I said, poorly designed... I also had to fix some minor issues around in the models so it looked like a good moment to do some refactoring.
On top of it, looking around the web, I found [this](https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-sqlalchemy){:target="_blank"}, compared the defined relationships in those models and mines and it looked like my relationships were completely different, I honestly don't remember where I read about the previous code, but anyway after testing the new code, it was working fine so I decided to keep it.
Back to my models, I decided to create two new models, IngredientQuantity and ManufactoredIngredientQuantity, so I could relate them with every other table that require a quantity, from placed orders and deliveries and wastages of Ingredients to the sale, preparation or wastage of one or more ManufactoredIngredients (as long has they are flagged as sellable and their price is set).
Once I was at it I decided to rename some variables in a more semantic way and to add two new columns in the BoardMessage model for the message's subject and its replies.

#### Bugs in development - Commit [1](https://github.com/antoniobruchidev/mp3-restaurant-manager/commit/6dcafa5633f49ba5f6c9f13584c14b9a3180b825){:target="_blank"}

I started developing it using wtforms, but I had trouble changing the values of select fields with javascript, so at the beginning I tought of having the select field to be choosen manually and when the user would select an option have it populate the form accordingly, because I couldn't find a way to populate a hidden field, so the result was clearly not good for user experience. From there the decision to quit using wtforms and let javascript handle the rest.

#### Other bugs

Almost ninthy percent of the bugs solved are due mistyping and in this kind of project.

### Testing

#### HTML checker
https://validator.w3.org/nu/?doc=https%3A%2F%2Fcarpez-kitchen-manager-e9e93ef660cf.herokuapp.com%2F

#### Color checker
https://webaim.org/resources/contrastchecker/?fcolor=FFFFDB&bcolor=A52A2A
https://webaim.org/resources/contrastchecker/?fcolor=FFFFDB&bcolor=A52A2A

### Deployement

The platform is deployed on heroku and code stored on github for comparison.
Deploying procedure is semi automatic once we connect the github repo to heroku.
Set DEBUG to False.