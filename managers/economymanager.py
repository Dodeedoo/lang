import operator
from data import database
from data.database import db
import base64


class Wallet:
    users = {}
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "/": operator.truediv,
        "*": operator.mul,
        "**": operator.pow
    }

    def __init__(self, money, inventory):
        self.money = money
        self.inventory = inventory

    def get_money(self, formatted=True):
        if formatted:
            return format(self.money, ",")
        return self.money

    def add(self, amount):
        self.money += amount

    def remove(self, amount):
        self.money -= amount

    # example: operate(100, "*") = money * 100
    def operate(self, amount, symbol):
        Wallet.operators[symbol](self.money, amount)


def load_user(id):
    table = database.create_user_table(id)
    try:
        user = db.session.query(table).filter(table.id == id).one()
        inv = ''
        if user.inventory != '' or None:
            inv = base64.decodestring(user.inventory)
        Wallet.users[id] = Wallet(user.balance, inv)
    except:
        print("ERROR while loading a user (most likely not registered in DB or User already loaded)")
