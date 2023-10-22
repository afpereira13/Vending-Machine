import unittest
from database_service import DatabaseService


class DatabaseServiceTest(unittest.TestCase):
    def setUp(self):
        self.database_service = DatabaseService("postgres_tests")

    def test_get_products(self):
        self.assertEqual(len(self.database_service.get_products()), 8)

    def test_get_product_price(self):
        result = self.database_service.get_product_price("watter_small")
        expect = ('1p',)
        self.assertEqual(result, expect)

    def test_update_product_price(self):
        rows_updated = self.database_service.update_product_price("watter_small", '2p')
        result = self.database_service.get_product_price("watter_small")
        expect = ('2p',)
        self.database_service.update_product_price("watter_small", '1p')
        self.assertEqual(rows_updated, 1)
        self.assertEqual(result, expect)

    def test_update_nonexistent_product_price(self):
        result = self.database_service.update_product_price("bananas", '2p')
        self.assertEqual(result, 0)

    def test_insert_and_remove_product(self):
        number_of_products = len(self.database_service.get_products())
        self.database_service.insert_new_product("bananas", 5, '7p')
        number_of_products_insert = len(self.database_service.get_products())
        self.database_service.delete_product("bananas")
        number_of_products_delete = len(self.database_service.get_products())

        self.assertEqual(number_of_products_insert, number_of_products+1)
        self.assertEqual(number_of_products_delete, number_of_products)

    def test_get_change(self):
        self.assertEqual(len(self.database_service.get_available_change()), 8)

    def test_update_available_change(self):
        rows_updated = self.database_service.update_available_change('2p', 1)
        rows_updated_remove_one = self.database_service.update_available_change('2p', -1)
        self.assertEqual(rows_updated, 1)
        self.assertEqual(rows_updated_remove_one, 1)

    def test_update_nonexistent_change(self):
        result = self.database_service.update_available_change('3p', -1)
        self.assertEqual(result, 0)

    def test_insert_and_remove_change(self):
        number_of_change = len(self.database_service.get_available_change())
        self.database_service.remove_change('2p')
        number_of_change_delete = len(self.database_service.get_available_change())
        self.database_service.insert_change('2p', 20)
        number_of_change_insert = len(self.database_service.get_available_change())

        self.assertEqual(number_of_change_delete, number_of_change-1)
        self.assertEqual(number_of_change_insert, number_of_change)

    def test_insert_sell_history(self):
        product = "sandwich"
        sell_history_size = len(self.database_service.get_sell_history())
        sell_history_product = len(self.database_service.get_sell_product_history(product))
        self.database_service.update_sell_history(product, "£2", "50")
        self.assertEqual(len(self.database_service.get_sell_history()), sell_history_size+1)
        self.assertEqual(len(self.database_service.get_sell_product_history(product)), sell_history_product+1)

if __name__ == '__main__':
    unittest.main()
