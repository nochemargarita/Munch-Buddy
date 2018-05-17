# import requests
# import json
# from pprint import pprint
from model import connect_to_db, db, User, Like, Restaurant, Category, RestaurantCategory, Message
from server import app
from werkzeug.security import generate_password_hash
from datetime import datetime
from datacollector import open_json_file, get_categories, get_restaurants


# Category
def add_category_to_db():
    """Add categories to the database."""
    for category in categories:
        cat_alias = categories[category]['cat_alias']
        cat_title = categories[category]['cat_title']

        cat = Category(cat_title=cat_title, cat_alias=cat_alias)

        db.session.add(cat)
    db.session.commit()


# RestaurantCategory
def add_rest_cat_to_db():
    """Add the restaurant id and category id to the database."""
    categorie = Category.query.all()

    for category in categorie:
        for restaurant in rest:
            for item in restaurant['categories']:
                cat_alias = category.cat_alias
                if cat_alias in item.values():
                    rest_cat = RestaurantCategory(rest_id=restaurant['id'],
                                                  cat_id=category.cat_id)
                    db.session.add(rest_cat)
    db.session.commit()


# Restaurant
def add_rest_to_db():
    """Add all restaurants and info to the database."""

    for restaurant in restaurants:
        info = restaurants[restaurant]
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


# User
def add_user_to_db(email, password, fname, lname, birthday):
    """Add fake users to database."""

    birthday = datetime.strptime(birthday, '%Y-%m-%d')
    password = generate_password_hash(password)
    user = User(email=email, password=password, fname=fname, lname=lname, birthday=birthday)

    db.session.add(user)
    db.session.commit()


# Message
def add_messages_to_db(from_user_id, to_user_id, messaged_on, message):
    """Add fake messages to database."""

    message = Message(from_user_id=from_user_id, to_user_id=to_user_id,
                      messaged_on=messaged_on, message=message)

    db.session.add(message)
    db.session.commit()


# Match

if __name__ == "__main__":
    connect_to_db(app)

    categories = get_categories('restaurants.json')
    restaurants = get_restaurants('restaurants.json')
    rest = open_json_file('restaurants.json')

    # add_user_to_db('marry@yahoo.com', '123', 'Mary', 'Poppins', '1965-08-25')
    # add_user_to_db('james@hotmail.com', '123', 'James', 'Corden', '1965-05-09')
    # add_user_to_db('hannah@gmail.com', '123', 'Hannah', 'Baker', '1945-02-05')
    # add_user_to_db('chris@gmail.com', '123', 'Chris', 'Hemsworth', '1989-06-15')

    # add_messages_to_db(1, 3, '2018-05-12', 'Hello, would you be down to eat some korean food?')
    # add_messages_to_db(3, 2, '2018-05-12', 'Yeah, that sounds really great. Do you have a restaurant in mind?')
    # add_messages_to_db(3, 4, '2018-05-12', 'Hi Man, saw you like ethipian food. WOuld you wanna grab sometime this week?')
    # add_rest_cat_to_db()
    # add_rest_to_db()
    # add_category_to_db()



