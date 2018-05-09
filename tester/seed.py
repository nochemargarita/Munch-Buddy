import requests
import os
import json
from model import connect_to_db, db, User, Like, Restaurant, Category
from server import app


API_KEY = os.environ['API_KEY'].strip()

def request_api_restaurants(offset):
    """Returns a json of request from Yelp API."""

    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer {key}'.format(key=API_KEY)}
    params = {'term': 'restaurants',
              'location': 'San Francisco',
              'offset': offset,
              'limit': 50
              }

    return requests.request('GET', url=url, headers=headers, params=params)

def restaurant_json_file():
    """Send response from API request to a text file."""

    file = open('restaurants.json', 'w')
    # look at restaurants.json

    offset = 0
    while offset < 951:
        # print offset
        response = request_api(offset)
        try:
            file.write(response.json()['businesses'] +'\n')
            # no need to use json.dumps
        except KeyError:
            print response.json()
        offset += 50

    file.close()

def get_categories(filename):
    """Get all restaurant categories from a text file."""
    # must import here if not using the file.json
    categories = []
    with open(filename) as filename:
        # for item in json.loads(open(filename))
        for item in filename:
           for indx in range(len(json.loads(item))):
                categories.append(json.loads(item)[indx]['categories'])
# cat += item[categories] -->array
    return categories

def get_categories_alias():
    """Get all unique alias categories."""

    alias_categories = []
    for i in get_categories('restaurants.txt'):
        for x in range(len(i)):
             if i[x]['alias'] not in alias_categories:
                alias_categories.append(i[x]['alias'])
# filter list cat by name
# helper function depends on
    return alias_categories

def add_categories_to_db():
    """Add all categories alias to database."""

    for alias in get_categories_alias():
        category = Category(cat_name=alias)

        db.session.add(category)

    db.session.commit()


# call this function only once. Comment Out after running once.
restaurant_json_file()
if __name__ == "__main__":
    connect_to_db(app)
    # db.create_all()

    # add_categories_to_db()
