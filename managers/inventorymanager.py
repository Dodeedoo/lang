import datetime
import traceback
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

    def __init__(self, emoji, min, max, price, name, gid, iid):
        if iid == "":
            self.itemid = str(uuid.uuid4())
        else:
            self.itemid = iid
        self.emoji = emoji
        self.min = min
        self.max = max
        self.price = price
        self.name = name
        self.history = MarketHistory(price)
        self.gid = gid

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

    def get_gid(self):
        return self.gid

    def set_price(self, amount):
        self.price += amount


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


def update_db_item(user: MarketItem, id):
    table = database.create_item_table(user.get_gid())
    try:
        itemdb = db.session.query(table).filter(table.id == id).one()
        print(str(id) + " refreshed into DB")
        itemdb.id = id
        itemdb.name = user.get_name()
        itemdb.min = user.get_min()
        itemdb.max = user.get_max()
        itemdb.emoji = user.get_emoji()
        itemdb.price = user.get_price()
        db.session.commit()
    except:
        traceback.print_exc()
        print("ERROR while loading a user (most likely not registered in DB or User already loaded)")


def get_item_from_name(name):
    for entry in MarketItem.items:
        print(entry)
        entry = MarketItem.items.get(entry)
        print(entry.get_name())
        if entry.get_name() == name:
            return entry


def check_if_loaded(gid):
    table = db.session.query(database.create_item_table(gid)).all()
    for entry in table:
        id = entry.id
        if MarketItem.items.get(id) is None:
            print("loading " + entry.id + " " + entry.name)
            load_item(id, gid)


def load_item(id, gid):
    table = database.create_item_table(gid)
    try:
        item = db.session.query(table).filter(table.id == id).one()
        print("queried")
        loaded = MarketItem(name=item.name, min=item.min, max=item.max, emoji=item.emoji, price=item.price, gid=gid, iid=id)
        MarketItem.items[id] = loaded
    except:
        print("error occured while loading an item from DB")


def register_item(min, max, emoji, price, name, gid):
    obj = MarketItem(emoji=emoji, min=min, max=max, price=price, name=name, gid=gid, iid="")
    db.session.add(database.create_item_table(gid)(
        id=obj.get_id(), name=name,
        min=min, max=max,
        emoji=emoji, price=price
    ))
    db.session.commit()

    load_item(obj.get_id(), gid)
