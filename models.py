from pony.orm import *
from flask_login import UserMixin
from datetime import datetime

db = Database(provider='postgres', user='rbxvkjjjszomhu', password='52a449ad3e0a5e874ab4f9a09dd1aa8139a888834bce7f58f7c0bba5ac63ac69', host='ec2-46-137-91-216.eu-west-1.compute.amazonaws.com', database='dehbguut8k9se2')


class User(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    login = Required(str)
    email = Required(str)
    pwd = Required(str)
    is_compiler = Required(bool, default=False)
    scores = Set('Score')
    dish_in_order = Set('Dish', reverse='users')
    order_compiler = Set('Dish', reverse='compiler')
    transactions = Set('Transaction')
    money = Required(int, default=0)


class Dish(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    description = Required(str)
    type_of_food = Required(str)
    scores = Set('Score')
    users = Set('User')
    price = Optional(int)
    small = Optional(str)
    cover = Optional(str)
    compiler = Required(User)


class Score(db.Entity):
    id = PrimaryKey(int, auto=True)
    dish = Required(Dish)
    user = Required(User)
    value = Optional(int)
    text = Optional(str)
    dt = Required(datetime)


class Transaction(db.Entity):
    id = PrimaryKey(int, auto=True)
    type = Required(str)
    value = Required(int)
    user = Required(User)
    description = Optional(str)
    dt = Required(datetime)
