import operator
import traceback

from data import database
from data.database import db
import base64

from managers import inventorymanager


class Wallet:
    users = {}
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "/": operator.truediv,
        "*": operator.mul,
        "**": operator.pow
    }

    def __init__(self, money, inventory: dict):
        self.money = money
        self.inventory = inventory

    def get_money(self, formatted=True):
        if formatted:
            return format(self.money, ",")
        return int(self.money)

    def add(self, amount):
        self.money += amount

    def remove(self, amount):
        self.money -= amount

    # example: operate(100, "*") = money * 100
    def operate(self, amount, symbol):
        self.money = Wallet.operators[symbol](self.money, amount)

    def get_inventory(self):
        return dict(self.inventory)

    def set_inventory(self, inventory):
        self.inventory = inventory


def mod_inventory(inventory: dict, operation: str, itemid: str, amount: int):
    print(inventory)
    item = inventory[itemid]
    if item is not None:
        if operation == "add":
            item[itemid].add(amount)
        else:
            item[itemid].remove(amount)
    else:
        if operation != "remove":
            inventory[itemid] = inventorymanager.get_as_invitem(id=itemid, amount=amount)

    return inventory


def load_user(id, gid):
    table = database.create_user_table(gid)
    try:
        user = db.session.query(table).filter(table.id == id).one()
        print("queried")
        inv = {}
        import json
        if user.inventory != '' or None:
            inv = json.loads(base64.decodestring(user.inventory))
        Wallet.users[id] = Wallet(user.balance, inv)
    except:
        traceback.print_exc()
        print("ERROR while loading a user (most likely not registered in DB or User already loaded)")


def check_if_loaded(id, gid):
    if Wallet.users.get(id) is None:
        print("user isnt loaded")
        load_user(id, gid)
