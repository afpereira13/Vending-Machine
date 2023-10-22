import unittest
import sys
from database_service import DatabaseService
from vending_machine_service import VendingMachineService

sys.path.append('../database_service')


class VendingMachineServiceTest(unittest.TestCase):
    def setUp(self):
        self.database_service = DatabaseService("postgres_tests")
        self.vending_machine = VendingMachineService(self.database_service)

    def test_product_consumption(self):
        result = self.vending_machine.consume_product("apple", "10p")
        expect = True, 5, ["5p"]
        self.database_service.update_quantity("apple", 1)
        self.assertEqual(result, expect)

    def test_product_consumption_direct_coin_change_unavailable(self):
        self.database_service.remove_change("5p")
        result = self.vending_machine.consume_product("apple", "10p")
        expect = True, 5, ["1p", "1p", "1p", "1p", "1p"]
        self.database_service.insert_change("5p", 20)
        self.database_service.update_available_change("1p", 5)
        self.database_service.update_quantity("apple", 1)
        self.assertEqual(result, expect)

    def test_product_consumption_change_unavailable(self):
        result = self.vending_machine.consume_product("apple", "£10000000")
        expect = False, 999999995, "No change available!"
        self.assertEqual(result, expect)

    def test_unavailable_product_consumption(self):
        result = self.vending_machine.consume_product("soda", "10p")
        expect = False, 0, "Item Not Available"
        self.database_service.update_quantity("apple", 1)
        self.assertEqual(result, expect)

    def test_lack_of_money_consumption(self):
        result = self.vending_machine.consume_product("apple", "1p")
        expect = False, 4, "Price is higher than the inserted money!"
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
