currency_dict = {1: '1p', 2: '2p', 5: '5p', 10: '10p', 20: '20p', 50: '50p', 100: '£1', 200: '£2'}


def currency(value):
    if str(value).startswith("£"):
        return int(value.replace("£", "")) * 100
    elif str(value).endswith("p"):
        return int(value.replace("p", ""))
    else:
        return -1


def available_change_to_dict(available_change):
    available_change_dict = {}
    for change in available_change:
        available_change_dict[change[1]] = change[2]
    return available_change_dict


class VendingMachineService:

    def __init__(self, database):
        self.db_service = database
        self.items = self.db_service.get_products()

    def available_products(self):
        items_dict = {}
        for item in self.db_service.get_products():
            items_dict[item[1]] = {"quantity": item[2], "price": item[3]}
        return items_dict

    def maybe_allowed_purchase(self, product, payment):
        if product not in self.available_products().keys():
            return False, 0, "Item Not Available"
        price = currency(self.db_service.get_product_price(product)[0])
        payment = currency(payment)
        if price > payment or price == -1 or payment == -1:
            return False, price - payment, "Price is higher than the inserted money!"
        price_diff = payment - price
        change = self.return_change(price_diff)
        if not change:
            return False, payment - price, "No change available!"
        change_list = []
        for k, v in change.items():
            change_list += [k] * v
        return True, price_diff, change_list

    def consume_product(self, product, payment):
        allow, payment_diff, change = self.maybe_allowed_purchase(product, payment)
        if allow:
            self.db_service.update_quantity_consume_one(product)
            price = (currency(payment) - payment_diff) / 100
            self.db_service.update_sell_history(product, f"£{price}", payment_diff)
        return allow, payment_diff, change

    def remove_product(self, product):
        return self.db_service.delete_product(product)

    def update_product_price(self, item, price):
        return self.db_service.update_product_price(item, price)

    def update_product_quantity(self, item, quantity):
        return self.db_service.update_quantity(item, quantity)

    def get_available_change(self):
        return self.db_service.get_available_change()

    def insert_change(self, coin, quantity):
        return self.db_service.insert_change(coin, quantity)

    def update_change(self, coin, quantity):
        return self.db_service.update_available_change(coin, quantity)

    def return_change(self, value):
        change_coins = {}
        available_change = available_change_to_dict(self.get_available_change())
        if value in currency_dict.keys() and currency_dict[value] in available_change.keys():
            self.update_change(currency_dict[value], -1)
            return {currency_dict[value]: 1}
        else:
            for coin_value, coin_name in currency_dict.items():
                if coin_name in available_change.keys():
                    amount = available_change[coin_name]
                    if amount > 0:
                        needed_coins = value // coin_value
                        if amount > needed_coins:
                            change_coins[coin_name] = needed_coins
                            value -= coin_value * needed_coins
        if value > 0:
            return False
        for coin, amount in change_coins.items():
            self.update_change(coin, -1 * amount)
        return change_coins

    def sell_history(self):
        return self.db_service.get_sell_history()

    def get_sell_product_history(self, item):
        return self.db_service.get_sell_product_history(item)

    def close(self):
        self.db_service.close()
