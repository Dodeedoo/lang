import datetime
import uuid
from data import database
from data.database import db


class InventoryItem:

    def __init__(self, itemid, emoji, amount, name):
        self.itemid = itemid
        self.emoji = emoji
        self.amount = amount
        self.name = name

    def get_emoji(self):
        return self.emoji

    def get_id(self):
        return self.itemid

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def add(self, amount):
        self.amount += amount

    def remove(self, amount):
        self.amount -= amount



class MarketItem:
    # key: id, value: object
    items = {}

    def __init__(self, emoji, min, max, price, name):
        self.itemid = str(uuid.uuid4())
        self.emoji = emoji
        self.min = min
        self.max = max
        self.price = price
        self.name = name
        self.history = MarketHistory(price)

    def get_emoji(self):
        return self.emoji

    def get_id(self):
        return self.itemid

    def get_name(self):
        return self.name

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_price(self):
        return self.price

    def get_history(self):
        return self.history


class MarketHistory:
    """
    dataset index 0 = lowest, 19 = latest,
    every time an entry is given. 0 will be popped
    """

    def __init__(self, startingprice):
        self.dataset = {datetime.datetime.now(): startingprice}

    def add_entry(self, price):
        if len(self.dataset) >= 20:
            del self.dataset[next(iter(self.dataset))]
        self.dataset[datetime.datetime.now()] = price

    def get_history(self):
        return self.dataset


def get_as_invitem(id, amount):
    item = MarketItem.items.get(id)
    return InventoryItem(name=item.get_name(), itemid=id, amount=amount, emoji=item.get_emoji())


def load_item(id, gid):
    table = database.create_item_table(gid)
    try:
        item = db.session.query(table).filter(table.id == id).one()
        print("queried")
        loaded = MarketItem(name=item.name, min=item.min, max=item.max, emoji=item.emoji, price=item.price)
        MarketItem.items[id] = loaded
    except:
        print("error occured while loading an item from DB")


def register_item(min, max, emoji, price, name, gid):
    obj = MarketItem(emoji=emoji, min=min, max=max, price=price, name=name)
    db.session.add(database.create_item_table(gid)(
        id=obj.get_id(), name=name,
        min=min, max=max,
        emoji=emoji, price=price
    ))
    db.session.commit()

    #if you are reading this, that means I forgot to remove this line of debug code lol
    load_item(obj.get_id(), '845734294487171124')
