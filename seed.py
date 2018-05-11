import requests
import os
import json
from model import connect_to_db, db, User, Like, Restaurant, Category
from server import app
from pprint import pprint, pformat
from datetime import datetime


API_KEY = os.environ['API_KEY'].strip()
LIMIT_MAX_REQUEST = 50
OFFSET_MAX_PULL = 1000
# User
def add_user_to_db(email, password, fname, lname, birthday):
    birthday = datetime.strptime(birthday, '%Y-%m-%d')
    user = User(email=email, password=password, fname=fname, lname=lname, birthday=birthday)

    db.session.add(user)
    db.session.commit()

# Category
def cat_info(filename):
    """Get category id, title, alias from json file."""
    checker = []
    categories = {}
    with open(filename) as filename:
        for item in json.load(filename):
            if 'restaurants' in item['parents']:
                # if item['alias'] not in categories:
                bl = item.get('country_blacklist')
                wl = item.get('country_whitelist')
                if not bl and not wl:
                    categories[item['alias']] = {'alias': item['alias'],
                                                 'title': item['title']}
                elif bl:
                    if 'US' not in bl:
                        categories[item['alias']] = {'alias': item['alias'],
                                                 'title': item['title']}

    return categories

# for i in cat_info('categories.json'):
#     print i, len(cat_info('categories.json'))

def add_cat_to_db():
    """Add all categories to database."""
    # Category.query.delete()
    for category in categories:
        info = categories[category]
        cat = Category(cat_title=info['title'],
                       cat_alias=info['alias'])

        db.session.add(cat)
    db.session.commit()

# Restaurant
def request_api_restaurants(offset):
    """Request restaurants from Yelp API."""

    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer {key}'.format(key=API_KEY)}
    params = {'term': 'restaurants',
              'location': 'San Francisco',
              'offset': offset,
              'limit': LIMIT_MAX_REQUEST
              }

    return requests.request('GET', url=url, headers=headers, params=params)

def rest_json_file():
    """Send response from API request to a json file."""

    with open('restaurants.json', 'w') as filename:
        for off in range(0, OFFSET_MAX_PULL - LIMIT_MAX_REQUEST + 1, LIMIT_MAX_REQUEST):
            print off
            response = request_api_restaurants(off)
            businesses = response.json()['businesses']
            try:
                for indx in range(len(businesses)):
                    filename.write(json.dumps(businesses[indx]) + '\n')
            except KeyError:
                print response.json()


def get_restaurants_info(filename):
    """Get all restaurants from the json file."""
    restaurants = {}
    with open(filename, 'r') as filename:
        for item in filename:
            info = json.loads(item)
               
            restaurants[info['alias']] = {'rest_id': info['id'],
                                          'rest_title': info['name'],
                                          'rest_alias': info['alias'],
                                          'rating': info['rating'],
                                          'num_reviews': info['review_count'],
                                          'address': info['location']['display_address'],
                                          'phone': info['phone']
                                         }

    return restaurants


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
    # db.create_all()
    categories = cat_info('categories.json')
    rest_info = get_restaurants_info('restaurants.json')
    # add_user_to_db('m@yahoo.com', 'hello', 'man', 'doe', '1965-08-25')
    # add_user_to_db('j@hotmail.com', 'hi', 'King', 'hacks', '1965-05-09')
    # add_user_to_db('h@gmail.com', 'bye', 'Hot', 'Dog', '1945-02-05')

    # add_rest_to_db()
    # add_cat_to_db()
