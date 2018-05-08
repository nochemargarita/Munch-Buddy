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

    file = open('fin.txt', 'w')

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


def add_to_db():
    pass



# Call all necessary functions below
to_text_file()
