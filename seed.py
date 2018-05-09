import requests
import os
import json

API_KEY = os.environ['API_KEY'].strip()

def request_api(offset):
    """Returns a json of request from Yelp API."""

    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer {key}'.format(key=API_KEY)}
    params = {'category': 'Restaurant',
              'location': 'San Francisco',
              'offset': offset,
              'limit': 50
              }

    return requests.request('GET', url=url, headers=headers, params=params)

def to_text_file():
    """Puts response from API request to a text file."""

    file = open('restaurants.txt', 'w')

    offset = 0
    while offset < 951:
        # print offset
        response = request_api(offset)
        try:
            file.write(json.dumps(response.json()['businesses'])+'\n')
        except KeyError:
            print response.json()
        offset += 50

    file.close()

def get_categories(filename):
    """Get all restaurant categories from a text file."""

    categories = []
    with open(filename) as filename:
        
        for i in filename:
           for x in range(len(json.loads(i))):
                categories.append(json.loads(i)[x]['categories'])

    return categories

def add_categories_to_db():
    """Add all categories alias to database."""

    alias_categories = []
    for i in get_categories('restaurants.txt'):
        for x in range(len(i)):
             if i[x]['alias'] not in alias_categories:
                alias_categories.append(i[x]['alias'])

    for i in sorted(alias_categories):
        print i

add_categories_to_db()


# add_categories_to_db()

def add_to_db():
    pass

# call this function only once. Comment Out after running once.
# to_text_file()