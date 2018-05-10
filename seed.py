import requests
import os
import json
from model import connect_to_db, db, User, Like, Restaurant, Category
from server import app


API_KEY = os.environ['API_KEY'].strip()
# Category
def cat_info(filename):
    """Get category id, title, alias from json file."""
    checker = []
    categories = {}
    with open(filename) as filename:
        for item in json.load(filename):
            # key error: 'US' in item['country_blacklist'], how to add this logic?
            if 'restaurants' in item['parents']:
                if item['alias'] not in categories:
                # checker.append(item['parents'])
                    categories[item['alias']] = {'alias': item['alias'],
                                                 'title': item['title']}
    # print checker
    return categories

categories = cat_info('categories.json')

def add_cat_to_db():
    """Add all categories to database."""

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
              'limit': 1
              }

    return requests.request('GET', url=url, headers=headers, params=params)

def rest_json_file():
    """Send response from API request to a json file."""

    file = open('restaurants.json', 'w')

    offset = 0
    while offset < 951:
        print offset
        response = request_api_restaurants(offset)
        businesses = response.json()['businesses']
        try:
            for indx in range(len(businesses)):
                file.write(json.dumps(businesses[indx]) + '\n')
        except KeyError:
            print response.json()
        offset += 50

    file.close()

rest_json_file()

# Restaurants
def get_restaurants_info(filename):
    """Get all restaurants from the json file."""
    restaurants = {}
    with open(filename) as filename:
        for item in filename:
            info = json.loads(item)
            if info['alias'] not in restaurants:
                restaurants[info['alias']] = {'id': info['id'],
                                              'name': info['name'],
                                              'alias': info['alias'],
                                              'location': info['location']['display_address'],
                                              'phone': info['phone'],
                                              'rating': info['rating']}

    return restaurants

# rest_info = get_restaurants_info('restaurants.json')
# get_restaurants_info('restaurants.json')

def add_rest_to_db():
    """Add all restaurants and info to the database."""

    for restaurant in rest_info:
        info = rest_info[restaurant]
        st, city, zipcode = info['location']['display_address']
        address = '{} {} {}'.format(st, city, zipcode)
        category = Restaurant(rest_id=info['id'],
                              rest_title=info['title'],
                              rest_alias=info['alias'],
                              address=address,
                              phone=info['phone'],
                              rating=info['rating'],
                              num_reviews=info['reviews'])

        db.session.add(category)

    db.session.commit()
# call this function only once. Comment Out after running once.
# rest_json_file()
if __name__ == "__main__":
    connect_to_db(app)
    # db.create_all()

    add_rest_to_db()
    add_cat_to_db()
