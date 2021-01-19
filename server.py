from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO, emit, join_room
from flask_uploads import UploadSet, configure_uploads, IMAGES

from werkzeug.security import generate_password_hash, check_password_hash

from model import connect_to_db, db, User, LikeCategory, Category
from model import Message, LikeRestaurant

from matches import create_room_session, selected_category_name, get_profile_picture
from matches import query_user_in_session, query_message_session, get_all_restaurants
from matches import query_message_of_matches, map_selected_category, map_each_matched_user
from matches import join_categories

from random import choice
from string import ascii_letters

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images/profile-pictures'
configure_uploads(app, photos)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "munch_buddy_secret"

socketio = SocketIO(app)
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Homepage."""
    if 'user_id' in session:
        return redirect('/munchbuddies')
    else:
        return render_template("homepage.html")


@app.route('/signup', methods=['POST'])
def signup():
    """Process signup using post request."""

    username = request.form.get('username')
    password = request.form.get('password')
    display_name = request.form.get('display_name')
    interests = request.form.get('interests')

    hashed_password = generate_password_hash(password)
    new_user = db.session.query(User).filter(User.username == username).first()

    if new_user is not None:
        flash('Username is already taken.')
        return redirect('/')

    else:
        flash('Yay! You are now a Munch Buddy!')
        user = User(username=username, password=hashed_password,
                    display_name=display_name, interests=interests)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
    return render_template('upload.html')

def random_string():
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = ascii_letters
    return ''.join(choice(letters) for i in xrange(4))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Allows the user to upload profile picture."""

    if session.get('username'):
        username = session.pop('username')
        user = db.session.query(User).filter(User.username == username).first()
        session['user_id'] = user.user_id
        session['name'] = user.display_name
        user_id = session.get('user_id')
        url = str(user_id) + random_string() + ".jpg"
        print 'enter'
        if request.method == 'POST' and 'photo' in request.files:
            request.files['photo'].filename = url
            filename = photos.save(request.files['photo'])
            user_session = User.query.get(user_id)
            user_session.profile_picture = app.config['UPLOADED_PHOTOS_DEST'] + '/' + url
            db.session.commit()
            print 'success'
        return redirect('/categories')
    else:
        flash('wrong')
        print 'error'
        return redirect('/')


@app.route('/login')
def login_form():
    """Redirects the user to log in form page."""
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Verify user and log the user in."""

    username = request.form.get('username')
    password = request.form.get('password')
    user = db.session.query(User).filter(User.username == username).first()

    if user:
        checked_hashed = check_password_hash(user.password, password)
        if checked_hashed:
            session['user_id'] = user.user_id
            session['name'] = user.display_name
            flash('You successfully logged in.')
            return redirect('/munchbuddies')
        else:
            flash('You have entered the wrong password!')
            return redirect('/')

    else:
        flash('Please check your username and password!')
        return redirect('/')


@app.route('/logout')
def logout():
    """Logs the user out from the session."""
    if session.get('user_id'):
        flash('You successfully logged out.')
        session.pop('user_id', None)
        return redirect('/')
    else:
        return redirect('/')


@app.route('/categories')
def categories():
    """Take all the categories of cuisine from database for user to choose from."""
    categories = Category.query.order_by(Category.cat_id).all()

    if session.get('user_id'):
        return render_template('/categories.html', categories=categories)

    else:
        return redirect('/')


@app.route('/categories', methods=['GET', 'POST'])
def selected_categories():
    """Get all selected check boxes and add it to database, LikeCategory."""

    user = User.query.get(session['user_id'])
    submitted_categories = request.form.getlist('cat_id')

    if submitted_categories:
        for ident in submitted_categories:
            like = LikeCategory(user_id=user.user_id, cat_id=ident)

            db.session.add(like)
        db.session.commit()
        return redirect('/munchbuddies')

    else:
        flash('Please choose 5.')
        return redirect('/categories')


@app.route('/saved-restaurants')
def saved_restaurants():
    """Redirect the user to saved restaurant/s."""
    if session.get('user_id'):
        name = session.get('name')
        profile_picture = get_profile_picture()

        return render_template('savedrestaurants.html', name=name, profile_picture=profile_picture)

    else:
        return redirect('/')


@app.route('/munchbuddies')
def show_buddies():
    """Directs user to a page with list of people who matched his/her choice of categories."""
    user_session_id = session.get('user_id')
    name = session.get('name')

    if user_session_id:
        profile_picture = get_profile_picture()
        results = get_all_restaurants()
        matches = {}
        matches_cat = join_categories()

        for user_id, restaurant in results.iteritems():
            user = query_user_in_session(user_id)
            session_id = query_message_session(user_id)
            matches_cat[user_id]

            if session_id:
                matches[user.user_id] = {'display_name': user.display_name,
                                         'interests': user.interests,
                                         'session_id': session_id.sess_id,
                                         'restaurant': choice(restaurant),
                                         'user_id': user_id,
                                         'profile_picture': user.profile_picture,
                                         'matches_cat': matches_cat[user_id]}
            else:
                create_room_session()

        return render_template('munchbuddies.html', matches=matches,
                               sess=user_session_id, profile_picture=profile_picture,
                               name=name, async_mode=socketio.async_mode)

    else:
        return redirect('/')


@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
    """Add the new liked restaurant of the user to LikeRestaurant database."""
    user_id = session.get('user_id')
    restaurant_id = request.form['data']

    if restaurant_id:
        current_likes = db.session.query(LikeRestaurant).filter(LikeRestaurant.user_id == user_id,
                                                                LikeRestaurant.rest_id == restaurant_id).first()

        if not current_likes:
            add_like_to_db = LikeRestaurant(user_id=user_id, rest_id=restaurant_id)
            db.session.add(add_like_to_db)
            db.session.commit()
            restaurant = {}

            new_liked_restaurant = db.session.query(LikeRestaurant).filter(LikeRestaurant.user_id == user_id,
                                                                           LikeRestaurant.rest_id == restaurant_id).first()

            restaurant[restaurant_id] = {'title': new_liked_restaurant.like_restaurant.rest_title,
                                         'url': new_liked_restaurant.like_restaurant.link,
                                         'image': new_liked_restaurant.like_restaurant.image_url
                                         }
            return jsonify(restaurant)


@app.route('/delete_liked_restaurant', methods=['POST'])
def delete_restaurant():
    """Delete user liked restaurant from database, LikeRestaurant."""
    restaurant_id = request.form['data']
    user_id = session.get('user_id')
    if restaurant_id:
        db.session.query(LikeRestaurant).filter(LikeRestaurant.user_id == user_id,
                                                LikeRestaurant.rest_id == restaurant_id).delete()
        db.session.commit()

    return restaurant_id


@app.route('/restaurants.json')
def show_restaurants():
    """Retrieve user liked restaurants from database."""
    user_id = session.get('user_id')
    current_likes = db.session.query(LikeRestaurant).filter(LikeRestaurant.user_id == user_id).all()
    restaurants = {}
    if current_likes:
        for restaurant in current_likes:
            restaurants[restaurant.rest_id] = {'title': restaurant.like_restaurant.rest_title,
                                               'url': restaurant.like_restaurant.link,
                                               'image': restaurant.like_restaurant.image_url
                                               }

    return jsonify(restaurants)


@app.route('/messages.json')
def show_messages():
    """Retrieve all messages of current user and buddies."""
    all_messages = {}
    results = get_all_restaurants()
    for user_id, restaurant in results.iteritems():
        session_id = query_message_session(user_id)

        if session_id:
            all_messages.update(query_message_of_matches(user_id))

    return jsonify(all_messages)


@app.route('/sender_name.json')
def get_sender_name():
    """jsonify the current user's name and profile picture."""

    name = session.get('user_id')
    display_name = session.get('name')

    pic = db.session.query(User).filter(User.user_id == name).first()
    info_of_sender = {'profile_picture': pic.profile_picture,
                      'display_name': display_name}
    return jsonify(info_of_sender)


@app.route('/matches_for_chat.json')
def session_id_for_matches():
    """Returns all the chat session ids related to the current user."""
    results = get_all_restaurants()
    chat_session_ids = []
    for user_id, restaurant in results.iteritems():
        session_id = query_message_session(user_id)

        if session_id:
            chat_session_ids.append(session_id.sess_id)

    return jsonify(chat_session_ids)


@socketio.on('join', namespace='/munchbuddies')
def join(message):
    """The user enters the chat room."""
    room = message['room']
    join_room(room)


@socketio.on('my_room_event', namespace='/munchbuddies')
def send_room_message(message):
    """Emits the message to the chat room when sent and then added to database, Message."""
    emit('my_response', message, room=message['room'])
    user_session_id = session.get('user_id')
    message_to_db = Message(sess_id=message['room'],
                            from_user_id=user_session_id,
                            to_user_id=message['receiver_id'],
                            message=message['data'])
    db.session.add(message_to_db)
    db.session.commit()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    # Run server in developer mode
    # socketio.run(app, debug=False, port=5000)
    # Run server in developer mode in vagrant
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
