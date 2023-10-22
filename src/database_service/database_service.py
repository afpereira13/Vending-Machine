import psycopg2


class DatabaseService:
    def connect_db(self, db_host='postgres'):
        self.db_connection = psycopg2.connect(database='vendingmachine',
                                              user='vending',
                                              host=db_host,
                                              password='m4CH!Ne')
        self.db_cursor = self.db_connection.cursor()

    def __init__(self, db_host='postgres'):
        self.db_connection = None
        self.db_cursor = None
        self.connect_db(db_host)

    def get_products(self):
        self.db_cursor.execute("SELECT * FROM vendingmachine WHERE quantity > 0")
        rows = self.db_cursor.fetchall()
        return rows

    def get_product_price(self, prod_name):
        self.db_cursor.execute(f"SELECT price FROM vendingmachine WHERE prod_name = '{prod_name}'")
        rows = self.db_cursor.fetchall()
        return rows[0]

    def update_product_price(self, prod_name, price):
        self.db_cursor.execute(f"UPDATE vendingmachine SET price = '{price}' "
                               f"WHERE prod_name = '{prod_name}'")
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def insert_new_product(self, prod_name, quantity, price):
        self.db_cursor.execute(
            f"INSERT INTO vendingmachine (prod_name, quantity, price) VALUES ('{prod_name}', {quantity}, '{price}')")
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def update_quantity_consume_one(self, prod_name):
        sql_update_query = f"Update vendingmachine set \
            quantity = (quantity-1) where prod_name = '{prod_name}'"
        self.db_cursor.execute(sql_update_query)
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def update_quantity(self, prod_name, insert_quantity):
        self.db_cursor.execute(f"UPDATE vendingmachine SET quantity = (quantity+'{insert_quantity}') "
                               f"WHERE prod_name = '{prod_name}'")
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def delete_product(self, prod_name):
        self.db_cursor.execute(f"DELETE FROM vendingmachine WHERE prod_name = '{prod_name}'")
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def get_sell_history(self):
        self.db_cursor.execute("SELECT * FROM sellhistory")
        rows = self.db_cursor.fetchall()
        return rows

    def get_sell_product_history(self, prod_name):
        self.db_cursor.execute(f"SELECT * FROM sellhistory WHERE prod_name = '{prod_name}'")
        rows = self.db_cursor.fetchall()
        return rows

    def update_sell_history(self, prod_name, price, changegiven):
        self.db_cursor.execute(f"INSERT INTO sellhistory (prod_name, price, changegiven, sell_time) "
                               f"VALUES ('{prod_name}', '{price}', '{changegiven}', NOW())")
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def get_available_change(self):
        self.db_cursor.execute("SELECT * FROM changecoins WHERE quantity > 0")
        rows = self.db_cursor.fetchall()
        return rows

    def insert_change(self, coin, quantity):
        self.db_cursor.execute(f"INSERT INTO changecoins (coin, quantity) VALUES ('{coin}', {quantity})")
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def update_available_change(self, coin, quantity):
        self.db_cursor.execute(f"UPDATE changecoins SET quantity = (quantity+'{quantity}') "
                               f"WHERE coin = '{coin}'")
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def remove_change(self, coin):
        self.db_cursor.execute(f"DELETE FROM changecoins WHERE coin = '{coin}'")
        self.db_connection.commit()
        return self.db_cursor.rowcount

    def close(self):
        self.db_cursor.close()
        self.db_connection.close()
