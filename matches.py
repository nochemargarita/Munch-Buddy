from model import connect_to_db, db, User, LikeCategory, Restaurant, Category, RestaurantCategory, Message, MessageSession
# from server import app
from algorithm import pearson
from flask import session


def get_user_selected_category():
    """Returns a list of category ids that the current user selected/likes."""
    current_user_liked = LikeCategory.query.filter(LikeCategory.user_id == session.get('user_id')).all()

    return [item.cat_id for item in current_user_liked]


def map_selected_category():
    """Returns a list that contains 1 or 2.

       1 if current user did not select the category.
       2 if current user selected category.
    """
    categories = Category.query.all()
    current_user = []
    for category in categories:
        if category.cat_id in get_user_selected_category():
            current_user.append(2)
        else:
            current_user.append(1)

    return current_user


# Users from database.
def find_matched_users():
    """Returns a dictionary of users and an empty list."""
    users_like = LikeCategory.query.all()

    users = {}
    for user in users_like:
        user_id = user.user_id
        if user.user_id != session.get('user_id') and \
           user.user_id not in users:
            users[user_id] = []

    return users


# NEED TO OPTIMIZE, NESTED FOR LOOPS
def add_to_matched_users():
    """Returns a dictionary of users and list of chosen categories."""

    users = find_matched_users()
    for user in users:
        users_like = LikeCategory.query.filter(LikeCategory.user_id == user).all()
        for item in users_like:
            users[user].append(item.cat_id)

    return users


# NEED TO OPTIMIZE, NESTED FOR LOOPS
def map_each_matched_user():
    """Returns a list that contains 1 or 2.

       1 if matched user did not select the item.
       2 if matched user selected the item.
    """
    mapped_users = find_matched_users()
    users = add_to_matched_users()
    categories = Category.query.all()

    for user_id, val in users.iteritems():
        for category in categories:
            if category.cat_id in val:
                if user_id in mapped_users:
                    mapped_users[user_id].append(2)
            else:
                mapped_users[user_id].append(1)

    return mapped_users



def get_pearson_correlation():
    """Returns a pearson correlation between the current user and the matches."""

    mapped_users = map_each_matched_user()
    current_user = map_selected_category()

    results = {}
    for user_id, val in mapped_users.iteritems():
        total = pearson(zip(current_user, val))
        results[user_id] = total

    return results


# create a helper function to call the get pairs and returns the list of pearson correlation
def get_current_user_matches():
    """Returns a dictionary of users who scored .5 and above in the pearson correlation."""
    users = {}
    for user_id, score in get_pearson_correlation().iteritems():
        if score > .5:
            users[user_id] = []

    return users


# Finding a restaurant suggestion for user and his/her matches
def matches_liked_categories():
    """Returns a list of objects of each user's match selected categories."""

    users_and_restaurants = []
    for user_id, lst in get_current_user_matches().iteritems():
        liked = LikeCategory.query.filter(LikeCategory.user_id == user_id).all()
        users_and_restaurants.extend(liked)

    return users_and_restaurants


def matched_category():
    """Matched categories per user."""

    suggestions = {}
    for user in matches_liked_categories():
        if user.user_id not in suggestions:
            suggestions[user.user_id] = [user.cat_id]
        else:
            suggestions[user.user_id].append(user.cat_id)

    return suggestions


def query_restaurants_categories():
    """Returns a list of Restaurant object."""

    restaurants_obj = {}
    for user, category in matched_category().iteritems():
        for item in category:
            rest_cat = RestaurantCategory.query.filter(RestaurantCategory.cat_id == item).all()
            if user not in restaurants_obj:
                restaurants_obj[user] = rest_cat
            else:
                if rest_cat not in restaurants_obj[user]:
                    restaurants_obj[user].extend(rest_cat)

    return restaurants_obj


def get_rest_id():
    """Returns a list of restaurant ids."""

    restaurants = {}
    for user, rest_id in query_restaurants_categories().iteritems():
        for rest in rest_id:
            if user not in restaurants:
                restaurants[user] = [rest.rest_id]
            else:
                restaurants[user].append(rest.rest_id)

    return restaurants


def get_all_restaurants():
    """Returns obj"""
    restaurants = {}
    for user, rest_id in get_rest_id().iteritems():
        for rest in rest_id:
            restaurant = Restaurant.query.filter(Restaurant.rest_id == rest).one()
            if user not in restaurants:
                restaurants[user] = [{'rest_title': restaurant.rest_title,
                                     'rating': restaurant.rating,
                                     'num_reviews': restaurant.num_reviews,
                                     'address': restaurant.address,
                                     'phone': restaurant.phone,
                                     'link': restaurant.link,
                                     'image_url': restaurant.image_url,
                                     'rest_id': restaurant.rest_id
                                      }]
            else:
                restaurants[user].append({'rest_title': restaurant.rest_title,
                                          'rating': restaurant.rating,
                                          'num_reviews': restaurant.num_reviews,
                                          'address': restaurant.address,
                                          'phone': restaurant.phone,
                                          'link': restaurant.link,
                                          'image_url': restaurant.image_url,
                                          'rest_id': restaurant.rest_id
                                          })

    return restaurants


# add to database the pairs and give unique id
def create_room_session():

    for match in get_current_user_matches():
        pair = MessageSession.query.filter( ((MessageSession.from_user_id == session.get('user_id')) |
                                            (MessageSession.from_user_id == match)) &
                                            ((MessageSession.to_user_id == match) |
                                            (MessageSession.to_user_id == session.get('user_id'))) ).first()
        if not pair:
            new_pair = MessageSession(from_user_id=session.get('user_id'), to_user_id=match)
            db.session.add(new_pair)

    db.session.commit()


def query_user_in_session(user):
    """Returns an object of information about the current user in session."""
    user = User.query.filter(User.user_id == user).first()

    return user


def query_message_session(user_id):

    message_session = MessageSession.query.filter(((MessageSession.from_user_id == session.get('user_id')) |
                                       (MessageSession.from_user_id == user_id)) &
                                      ((MessageSession.to_user_id == user_id) |
                                       (MessageSession.to_user_id == session.get('user_id')))).first()
    return message_session


def query_message_of_matches(user_id):
    """Returns a dictionary of messages of current user and his/her matches."""

    all_messages = {}
    messages = Message.query.filter(Message.sess_id == query_message_session(user_id).sess_id).all()

    if messages:
        for message in messages:
            from_user_name = query_user_in_session(message.from_user_id)
            to_user_name = query_user_in_session(message.to_user_id)

            if message.sess_id not in all_messages:
                str_date = message.messaged_on.strftime('%a %b %d')
                all_messages[message.sess_id] = [{'from': from_user_name.profile_picture,
                                                  'to': to_user_name.profile_picture,
                                                  'message': message.message,
                                                  'date': str_date}]
            else:
                all_messages[message.sess_id].append({'from': from_user_name.profile_picture,
                                                      'to': to_user_name.profile_picture,
                                                      'message': message.message,
                                                      'date': str_date})

    return all_messages


def get_profile_picture():
    """Returns the path of current user's profile picture."""

    user = db.session.query(User).filter(User.user_id == session.get('user_id')).first()
    if user.profile_picture:
        return user.profile_picture
    else:
        return "static/img/blank.png"


def selected_category_name():
    """Get the current user's selected category names."""

    current_user_liked = LikeCategory.query.filter(LikeCategory.user_id == session.get('user_id')).all()

    return [item.category.cat_title for item in current_user_liked]





if __name__ == "__main__":
    connect_to_db(app)
    get_pearson_correlation()
    get_current_user_matches()
    matches_liked_categories()
    
    get_all_restaurants()
    create_room_session()
    get_profile_picture()
