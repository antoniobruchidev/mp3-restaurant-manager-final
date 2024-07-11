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

