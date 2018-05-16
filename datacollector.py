# from pprint import pprint
import requests
import json
import os


API_KEY = os.environ['API_KEY'].strip()
LIMIT_MAX_REQUEST = 50
OFFSET_MAX_PULL = 1000


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


def open_json_file(filename):
    """Open restaurants.json and append it to a list."""

    restaurants = []

    with open(filename, 'r') as filename:
        for item in filename:
            info = json.loads(item)
            restaurants.append(info)

    return restaurants


def get_restaurants(filename):
    """Get all restaurants from the json file."""
    restaurant_info = {}
    restaurants = open_json_file(filename)
    for restaurant in restaurants:
        restaurant_info[restaurant['alias']] = {'rest_id': restaurant['id'],
                                                'rest_title': restaurant['name'],
                                                'rest_alias': restaurant['alias'],
                                                'rating': restaurant['rating'],
                                                'num_reviews': restaurant['review_count'],
                                                'address': restaurant['location']['display_address'],
                                                'phone': restaurant['phone']
                                                }

    return restaurant_info


# Category
def append_categories(filename):
    """Get all restaurant categories from the json file."""
    category_info = []
    restaurants = open_json_file(filename)
    for category in restaurants:
        category_info.extend(category['categories'])

    return category_info


def get_categories(filename):
    """Get all unque categories."""

    category_info = {}
    categories = append_categories(filename)
    for cat in categories:
        alias = cat['alias']
        title = cat['title']
        # if alias[-4:] != 'bars':
            # print alias
        # if 'wine' != alias[-4:] and 'bars' != alias[-4:] and
        #    'shops' != alias[-5] and 'stores' != alias[-6] and
        #    'markets' != alias[-7]:
        if 'se' == alias[-2:] or 'an' == alias[-2:]:
            category_info[alias] = {'cat_alias': alias,
                                    'cat_title': title}

    return category_info



