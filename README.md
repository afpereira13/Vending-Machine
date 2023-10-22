# Vending-Machine
Programming Exercise: Vending Machine Exercise 
The goal is to design a vending machine using a programming language of my choice.

The vending machine should perform as follows:

- Once an item is selected and the appropriate amount of money is inserted, the vending machine should return the correct product. 
- It should also return change if too much money is provided, or ask for more money if insufficient funds have been inserted. 
- The machine should take an initial load of products and change. The change will be in denominations of 1p, 2p, 5p, 10p, 20p, 50p, £1, £2. There should be a way of reloading either products or changes at a later point.
- The machine should keep track of the products and change that it contains.

## Project Installation Instructions

### Using Docker
Run the following commands in the terminal to Builds, (re)creates, starts, and attaches to container for Vending-Machine service (vending_machine_app) :
```
docker compose up vending_machine_app
```

## How to use
Since the Vending-Machine is an API, start to check the available endpoints (check [API Documentation](#api-documentation))
To use any endpoint it is possible to make all the requests using API Documentation Page. In each endpoint, press the 'Try it out' button, and fill the values if needed.
But if you prefer use the terminal (curl) or use any API platform (e.g. Postman).

# Technical Description
The project is separated into 3 main parts:

1. The database (DB), database_service.py.
2. The vending machine, vending_machine_service.py.
3. The api, main.py.

## API
Since this exercise has the following requisite:
- The "project will be part of a more complex system, and it will be handed over to a team for maintenance and the development of new features."

An API is great to achieve the exercise goals, because allows it to have two different kinds of API endpoints:
- Common use, e.g. Check available products and buy one. All these endpoints starts with `/items/*`
- Admin use, e.g. Add more products or change. All these endpoints starts with `/admin/*`

API offers an abstraction layer to the user, stopping the DB access directly.

### API Documentation
Upon docker containers up, is possible to look through the API Documentation to know which endpoint are available and read a small description.
To access this documentation go to a web browser and use the following url http://localhost/docs/

## Vending-Machine Service
The vending_machine_service.py act as a bridge between the API and the DB, blocking the user from access the DB directly
The major goal is to take data from the DB and prepare it to be consumed by the API user.

This service takes all data needed from the API to operate

## Database Service
The DB is implemented using [Postgres](https://www.postgresql.org/). 
This open-source DB offers reliability, feature robustness, and performance.

It is used a single connection between the database_service and the DB. 
Because creating a connection can be slow (SSL over TCP), so the best practice is to create a single connection and keep it open as long as required.

The DB is composed by 3 tables:
- vendingmachine, each entry has the product representation, product's quantity, and product's price;
- changecoins, each entry has the coin representation, and coin's quantity;
- sellhistory, each entry has the product sell, product's price, change given (in pounds), and sell time.

# Testing

## Unit Tests
```
docker build -t test_some_module -f Dockerfile-Tests .
docker run -it --name test_some_module --rm test_some_module
```

# Future Targets
1. Implement authentication for all admin endpoints. Since common user should not be able to maintain the vending machine (e.g. add more products to the vending machine);
2. Keeping track of money given by users. Currently, the buy endpoint uses the total money as input, e.g. `£1.2`, and not a list of coins (to be passed in the body request);
3. Handle database failures in proper way, e.g. retry connection mechanism.
