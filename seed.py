import requests
import json
from model import connect_to_db, db, User, Like, Restaurant, Category, RestaurantCategory, Message
from server import app
from werkzeug.security import generate_password_hash
from datetime import datetime
from datacollector import cat_info, get_restaurants_info

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


# RestaurantCategory
def restaurant_category():
    """add restaurant and category to RestaurantCategory database."""

    like = Like.query.all()
    res = RestaurantCategory.query.all()
    print res
    with open('restaurants.json', 'r') as filename:
        for item in filename:
            info = json.loads(item)


            for i in range(len(info['categories'])):
                for indx in range(len(like)):
                    cat_alias = like[indx].category.cat_alias
                    if cat_alias in info['categories'][i]['alias']:
                        rest_cat = RestaurantCategory(rest_id=info['id'], cat_id=like[indx].cat_id)

                        db.session.add(rest_cat)

            db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    restaurant_category()
    # categories = cat_info('categories.json')

    # rest_info = get_restaurants_info('restaurants.json')
    # add_user_to_db('marry@yahoo.com', '123', 'Mary', 'Poppins', '1965-08-25')
    # add_user_to_db('james@hotmail.com', '123', 'James', 'Corden', '1965-05-09')
    # add_user_to_db('hannah@gmail.com', '123', 'Hannah', 'Baker', '1945-02-05')
    # add_user_to_db('chris@gmail.com', '123', 'Chris', 'Hemsworth', '1989-06-15')

    # add_messages_to_db(1, 3, '2018-05-12', 'Hello, would you be down to eat some korean food?')
    # add_messages_to_db(3, 2, '2018-05-12', 'Yeah, that sounds really great. Do you have a restaurant in mind?')
    # add_messages_to_db(3, 4, '2018-05-12', 'Hi Man, saw you like ethipian food. WOuld you wanna grab sometime this week?')

    # add_rest_to_db()
    # add_cat_to_db()
