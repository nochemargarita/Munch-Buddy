from pprint import pprint, pformat
import json
import os

API_KEY = os.environ['API_KEY'].strip()
LIMIT_MAX_REQUEST = 50
OFFSET_MAX_PULL = 1000


# Category
def cat_info(filename):
    """Get category id, title, alias from json file."""
    categories = {}
    with open(filename) as filename:
        for item in json.load(filename):
            if 'restaurants' in item['parents']:
                bl = item.get('country_blacklist')
                wl = item.get('country_whitelist')
                if item['alias'][-2::] == 'an' or item['alias'][-2::] == 'se':
                    if not bl and not wl:
                        categories[item['alias']] = {'alias': item['alias'],
                                                     'title': item['title']}
                    elif bl:
                        if 'US' not in bl:
                            categories[item['alias']] = {'alias': item['alias'],
                                                         'title': item['title']}

    return categories


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
