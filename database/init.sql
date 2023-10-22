CREATE TABLE vendingmachine (
    id serial PRIMARY KEY,
    prod_name VARCHAR(100) UNIQUE,
    quantity INTEGER,
    price VARCHAR(10)
);

INSERT INTO vendingmachine (prod_name, quantity, price) VALUES
    ('apple', 5, '5p'),
    ('cookies_chocolate', 5, '£1'),
    ('cookies_butter', 5, '50p'),
    ('chocolate_bar1', 10, '10p'),
    ('chocolate_bar2', 10, '20p'),
    ('sandwich', 5, '£2'),
    ('watter_small', 20, '1p'),
    ('watter_medium', 10, '2p');

CREATE TABLE changecoins (
    id serial PRIMARY KEY,
    coin VARCHAR(10) UNIQUE,
    quantity INTEGER
);

INSERT INTO changecoins (coin, quantity) VALUES
    ('1p', 20),
    ('2p', 20),
    ('5p', 20),
    ('10p', 20),
    ('20p', 20),
    ('50p', 20),
    ('£1', 20),
    ('£2', 20);

CREATE TABLE sellhistory (
    id serial PRIMARY KEY,
    prod_name VARCHAR(100),
    price VARCHAR(10),
    changegiven VARCHAR(10),
    sell_time timestamp
);