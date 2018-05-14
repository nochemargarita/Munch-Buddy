import requests
# import os
import json
from model import connect_to_db, db, User, Like, Restaurant, Category, RestaurantCategory, Message
from server import app
# from pprint import pprint, pformat
from datetime import datetime
from datacollector import cat_info, get_restaurants_info


# API_KEY = os.environ['API_KEY'].strip()
# LIMIT_MAX_REQUEST = 50
# OFFSET_MAX_PULL = 1000
# User
def add_user_to_db(email, password, fname, lname, birthday):
    """Add fake users to database."""

    birthday = datetime.strptime(birthday, '%Y-%m-%d')
    user = User(email=email, password=password, fname=fname, lname=lname, birthday=birthday)

    db.session.add(user)
    db.session.commit()


# Message
def add_messages_to_db():
    """Add fake messages to database."""

    pass


# Category
def add_cat_to_db():
    """Add all categories to database."""
    for category in categories:
        info = categories[category]
        cat = Category(cat_title=info['title'],
                       cat_alias=info['alias'])

        db.session.add(cat)
    db.session.commit()


# Restaurant
def add_rest_to_db():
    """Add all restaurants and info to the database."""

    for restaurant in rest_info:
        info = rest_info[restaurant]
        address = ', '.join(info['address'])

        category = Restaurant(rest_id=info['rest_id'],
                              rest_title=info['rest_title'],
                              rest_alias=info['rest_alias'],
                              rating=info['rating'],
                              num_reviews=info['num_reviews'],
                              address=address,
                              phone=info['phone']
                              )

        db.session.add(category)
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    categories = cat_info('categories.json')
    rest_info = get_restaurants_info('restaurants.json')
    # add_user_to_db('m@yahoo.com', 'hello', 'man', 'doe', '1965-08-25')
    # add_user_to_db('j@hotmail.com', 'hi', 'King', 'hacks', '1965-05-09')
    # add_user_to_db('h@gmail.com', 'bye', 'Hot', 'Dog', '1945-02-05')

    # add_rest_to_db()
    # add_cat_to_db()
