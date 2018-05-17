from model import connect_to_db, db, User, Like, Restaurant, Category, RestaurantCategory, Message
from server import app
    
NUM_PEOPLE_MATCHED = 5
# Current user in session.
def get_curr_user_liked(sess):
    """Returns a list of category id that current user likes."""
    current_user_liked = Like.query.filter(Like.user_id == sess).all()

    categories = []
    for i in current_user_liked:
        categories.append(i.cat_id)

    return categories


def track_liked(sess):
    """Returns a list that contains 1 or 2.

       1 if user did not like item.
       2 if user liked it.
    """
    categories = Category.query.all()
    current_user = []
    for category in categories:
        if category.cat_id in get_curr_user_liked(sess):
            current_user.append(2)
        else:
            current_user.append(1)

    return current_user

# Users from database.
def find_matched_users(sess):
    """Returns a dictionary of users and an empty list."""

    users_like = Like.query.all()

    users = {}
    for user in users_like:
        user_id = user.user_id
        if user.user_id != sess and \
           len(users) < NUM_PEOPLE_MATCHED and \
           user.user_id not in users:  # session.get('user_id')
            users[user_id] = []

    return users


def add_value_to_list(sess):
    """Returns a dictionary of users and list of chosen categories."""

    users = find_matched_users(sess)
    for user in users:
        users_like = Like.query.filter(Like.user_id == user).all()
        for item in users_like:
            users[user].append(item.cat_id)

    return users


def map_each_user(sess):
    """Returns a list that contains 1 or 2.

       1 if user did not like item.
       2 if user liked it.
    """
    mapped_users = find_matched_users(sess)
    users = add_value_to_list(sess)
    categories = Category.query.all()

    for user_id, val in users.iteritems():
        for category in categories:
            if category.cat_id in val:
                if user_id in mapped_users:
                    mapped_users[user_id].append(2)
            else:
                mapped_users[user_id].append(1)

    return mapped_users

# Pearson
from math import sqrt

def pearson(pairs):
    """Return Pearson correlation for pairs. -1..1"""

    series_1, series_2 = zip(*pairs)

    sum_1 = sum(series_1)
    sum_2 = sum(series_2)

    squares_1 = sum([n * n for n in series_1])
    squares_2 = sum([n * n for n in series_2])

    product_sum = sum([n * m for n, m in pairs])

    size = len(pairs)

    numerator = product_sum - ((sum_1 * sum_2) / size)

    denominator = sqrt(
                  (squares_1 - (sum_1 * sum_2) / size) *
                  (squares_2 - (sum_2 * sum_2) / size)
                  )

    return numerator / denominator


def get_pairs(sess):

    mapped_users = map_each_user(sess)
    current_user = track_liked(sess)
    results = {}

    for user_id, val in mapped_users.iteritems():
        total = pearson(zip(current_user, val))
        results[user_id] = total

    return results

if __name__ == "__main__":
    connect_to_db(app)
    # track_liked()
    # find_matched_users()
    # add_value_to_list()
    # map_each_user()
    print get_pairs(sess)
