from database_service import DatabaseService
from vending_machine_service import VendingMachineService
from fastapi import FastAPI, HTTPException, Path
from typing_extensions import Annotated
import json

app = FastAPI()
database_service = DatabaseService()
vending_machine = VendingMachineService(database_service)


@app.get("/admin/change")
def available_change():
    change_dict = {}
    for change in vending_machine.get_available_change():
        change_dict[change[1]] = change[2]
    return change_dict


@app.post("/admin/change/{coin}/quantity/{quantity}")
def insert_change_coin(coin: str, quantity: int):
    return vending_machine.insert_change(coin, quantity)


@app.put("/admin/change/{coin}/quantity/{quantity}")
def update_change_coin_quantity(coin: str, quantity: int):
    return vending_machine.update_change(coin, quantity)


@app.delete("/admin/change/{coin}")
def delete_change_coin(coin: str):
    return vending_machine.remove_coin(coin)


@app.get("/admin/sell_history")
def sell_history():
    return json.loads(json.dumps(vending_machine.sell_history(), ensure_ascii=False).encode('utf-8'))


@app.get("/admin/sell_history/item/{item}")
def sell_history_item(item: str):
    return json.loads(json.dumps(vending_machine.get_sell_product_history(item), ensure_ascii=False).encode('utf-8'))


@app.put("/admin/items/{item}/price/{price}")
def update_item_price(item: str, price: str):
    return vending_machine.update_product_price(item, price)


@app.put("/admin/items/{item}/quantity/{quantity}")
def update_item_quantity(item: str, quantity: Annotated[int, Path(ge=0)]):
    return vending_machine.update_product_quantity(item, quantity)


@app.delete("/admin/items/{item}")
def remove_item(item: str):
    return vending_machine.remove_product(item)


@app.get("/items")
def list_items():
    return vending_machine.available_products()


@app.post("/items/{item}/buy_insert_money/{money}")
def buy_item(item: str, money: str):
    allow, money_diff, change = vending_machine.consume_product(item, money)
    if not allow:
        raise HTTPException(status_code=400, detail=change)
    return {"message": f"You have bought 1 {item}", "change": change}
