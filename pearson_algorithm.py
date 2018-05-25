from model import connect_to_db, db, User, Like, Restaurant, Category, RestaurantCategory, Message, MessageSession
# from server import app

from math import sqrt


# Current user in session.
def get_curr_user_liked(sess):
    """Returns a list of category idq that current user likes."""
    current_user_liked = Like.query.filter(Like.user_id == sess).all()

    return [i.cat_id for i in current_user_liked]


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
           user.user_id not in users:
            users[user_id] = []

    return users


# NEED TO OPTIMIZE, NESTED FOR LOOPS
def add_value_to_list(sess):
    """Returns a dictionary of users and list of chosen categories."""

    users = find_matched_users(sess)
    for user in users:
        users_like = Like.query.filter(Like.user_id == user).all()
        for item in users_like:
            users[user].append(item.cat_id)

    return users


# NEED TO OPTIMIZE, NESTED FOR LOOPS
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

    denominator = sqrt((squares_1 - (sum_1 ** 2) / size) *
                  (squares_2 - (sum_2 ** 2) / size))

    return numerator / denominator

def get_pairs(sess):

    mapped_users = map_each_user(sess)
    current_user = track_liked(sess)

    results = {}
    for user_id, val in mapped_users.iteritems():
        total = pearson(zip(current_user, val))
        results[user_id] = total

    return results
    # return {user_id: pearson(zip(current_user, val)) for user_id, val in mapped_users.iteritems()}

# create a helper function to call the get pairs and returns the list of pearson correlation


def get_the_match(sess):
    """Returns a dictionary of users who scored .5 and above."""
    users = {}
    for user, score in get_pairs(sess).iteritems():
        if score > .5:
            users[user] = []

    return users


def get_liked_cat(sess):
    """Returns a list of user matched objects."""

    users_and_restaurants = []
    for user, lst in get_the_match(sess).iteritems():
        liked = Like.query.filter(Like.user_id == user).all()
        users_and_restaurants.extend(liked)

    return users_and_restaurants


def matched_category(sess):
    """Matched categories per user."""

    suggestions = {}
    for user in get_liked_cat(sess):
        if user.user_id not in suggestions:
            suggestions[user.user_id] = [user.cat_id]
        else:
            suggestions[user.user_id].append(user.cat_id)

    return suggestions


def query_restaurants_categories(sess):
    """Returns a list of Restaurant object."""

    restaurants_obj = {}
    for user, category in matched_category(sess).iteritems():
        for item in category:
            rest_cat = RestaurantCategory.query.filter(RestaurantCategory.cat_id == item).all()
            if user not in restaurants_obj:
                restaurants_obj[user] = rest_cat
            else:
                if rest_cat not in restaurants_obj[user]:
                    restaurants_obj[user].extend(rest_cat)

    return restaurants_obj


def get_rest_id(sess):
    """Returns a list of restaurant ids."""

    restaurants = {}
    for user, rest_id in query_restaurants_categories(sess).iteritems():
        for rest in rest_id:
            if user not in restaurants:
                restaurants[user] = [rest.rest_id]
            else:
                restaurants[user].append(rest.rest_id)

    return restaurants


def get_all_restaurants(sess):
    """Returns obj"""
    restaurants = {}
    for user, rest_id in get_rest_id(sess).iteritems():
        for rest in rest_id:
            restaurant = Restaurant.query.filter(Restaurant.rest_id == rest).one()
            if user not in restaurants:
                restaurants[user] = [{'rest_title': restaurant.rest_title,
                                     'rating': restaurant.rating,
                                     'num_reviews': restaurant.num_reviews,
                                     'address': restaurant.address,
                                     'phone': restaurant.phone
                                    }]
            else:
                restaurants[user].append({'rest_title': restaurant.rest_title,
                                          'rating': restaurant.rating,
                                          'num_reviews': restaurant.num_reviews,
                                          'address': restaurant.address,
                                          'phone': restaurant.phone
                                        })

    return restaurants


# add to database the pairs and give unique id
def create_session(sess):

    for match in get_the_match(sess):
        pair = MessageSession.query.filter( ((MessageSession.from_user_id == sess) |
                                            (MessageSession.from_user_id == match)) &
                                            ((MessageSession.to_user_id == match) |  
                                            (MessageSession.to_user_id == sess)) ).first()
        if not pair:
            new_pair = MessageSession(from_user_id=sess, to_user_id=match)
            db.session.add(new_pair)

    db.session.commit()


# def get_sess_id(sess):
#     for match in get_the_match(sess):
#         sess_id = MessageSession.query.filter( ((MessageSession.from_user_id == sess) |
#                                             (MessageSession.from_user_id == match)) &
#                                             ((MessageSession.to_user_id == match) |  
#                                             (MessageSession.to_user_id == sess)) ).first()
#     return sess_id.sess_id
if __name__ == "__main__":
    connect_to_db(app)
    # print get_curr_user_liked(3)
    # print track_liked(3)
    # print find_matched_users(3)
    # print add_value_to_list(3)
    # print map_each_user(3)
    # get_liked_cat()
    # print get_pairs(3)
    # get_all_restaurants(user_id)
    # show_rest_suggestions(sess)
    get_the_match(sess)
    # print get_liked_cat(3)
    # print query_restaurants_categories(3)
    # print get_rest_id(3)
    get_all_restaurants(sess)
    create_session(sess)
