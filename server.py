from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.security import generate_password_hash, check_password_hash
from model import connect_to_db, db, User, LikeCategory, Restaurant, Category, Message, MessageSession, RestaurantCategory, LikeRestaurant
from matches import create_room_session, selected_category_name, get_profile_picture, query_user_in_session, query_message_session, get_all_restaurants, query_message_of_matches

from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room, close_room, rooms
from flask_uploads import UploadSet, configure_uploads, IMAGES
from random import choice
from datetime import datetime


app = Flask(__name__)
# Images is the type of file that will be uploaded
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
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

    print username
    print password
    print display_name

    hashed_password = generate_password_hash(password)
    q = db.session.query(User).filter(User.username == username).first()

    if q:
        flash('Username is already taken.')
        return redirect('/signup')

    else:
        flash('Yay! You are now a Munch Buddy!')
        user = User(username=username, password=hashed_password,
                    display_name=display_name, interests=interests)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Allows the user to upload profile picture."""

    if session.get('username'):
        username = session.pop('username')
        user = db.session.query(User).filter(User.username == username).first()
        session['user_id'] = user.user_id
        session['name'] = user.display_name
        user_id = session.get('user_id')
        url = str(user_id) + ".jpg"

        if request.method == 'POST' and 'photo' in request.files:
            request.files['photo'].filename = url
            filename = photos.save(request.files['photo'])
            user_session = User.query.get(user_id)
            user_session.profile_picture = app.config['UPLOADED_PHOTOS_DEST'] + '/' + url
            db.session.commit()
        return redirect('/categories')
    else:
        flash('wrong')
        return redirect('/')


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
            return redirect('/login')

    else:
        flash('Please check your username and password!')
        return redirect('/login')


@app.route('/logout')
def logout():
    """Logs the user our from the session."""
    if session.get('user_id'):
        flash('You successfully logged out.')
        session.pop('user_id', None)
        return redirect('/')
    else:
        return render_template('/login.html')


@app.route('/categories')
def categories():
    """Let's the user select multiple categories of cuisine."""
    categories = Category.query.all()
    chosen_categories = selected_category_name()

    if session.get('user_id'):
        return render_template('/categories.html', categories=categories,
                               chosen_categories=chosen_categories)

    else:
        return redirect('/login')


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


@app.route('/munchbuddies')
def show_buddies():
    """Directs user to a page with list of people who matched his/her choice of categories."""
    sess = session.get('user_id')
    name = session.get('name')

    if sess:
        profile_picture = get_profile_picture()
        results = get_all_restaurants()
        matches = {}


        for user_id, restaurant in results.iteritems():
            user = query_user_in_session(user_id)
            session_id = query_message_session(user_id)

            if session_id:
                matches[user.user_id] = {'display_name': user.display_name,
                                         'interests': user.interests,
                                         'session_id': session_id.sess_id,
                                         'restaurant': choice(restaurant),
                                         'user_id': user_id,
                                         'profile_picture': user.profile_picture}

            else:
                create_room_session()

        return render_template('munchbuddies.html', matches=matches,
                               sess=sess, profile_picture=profile_picture,
                               name=name, async_mode=socketio.async_mode)

    else:
        return redirect('/login')


@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
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
    restaurant_id = request.form['data']
    user_id = session.get('user_id')
    if restaurant_id:
        db.session.query(LikeRestaurant).filter(LikeRestaurant.user_id == user_id,
                                                LikeRestaurant.rest_id == restaurant_id).delete()
        db.session.commit()

    return restaurant_id


@app.route('/restaurants.json')
def show_restaurants():
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
    all_messages = {}
    results = get_all_restaurants()
    for user_id, restaurant in results.iteritems():
        session_id = query_message_session(user_id)



        if session_id:
            all_messages.update(query_message_of_matches(user_id))

    return jsonify(all_messages)


@app.route('/editprofile')
def edit_profile():
    """Allows the user to edit interests and display name."""
    user_id = session.get('user_id')

    if user_id:
        interests = db.session.query(User).filter(User.user_id == user_id).first()

        return render_template('editprofile.html', interests=interests.interests,
                               display_name=interests.display_name, profile_picture=interests.profile_picture)

    else:
        return redirect('/')


@app.route('/editprofile', methods=['GET', 'POST'])
def update_edit_profile():
    """Update interests in the database."""
    user_id = session.get('user_id')
    interests = request.form.get('interests')
    display_name = request.form.get('display_name')
    if display_name or interests:
        db.session.query(User).filter(User.user_id == user_id).update(dict(interests=interests, display_name=display_name))
        db.session.commit()

        session.pop('name', None)
        session['name'] = display_name

    url = str(user_id)+"1" + ".jpg"
    if request.method == 'POST' and 'photo' in request.files:
            request.files['photo'].filename = url
            filename = photos.save(request.files['photo'])
            profile_picture = app.config['UPLOADED_PHOTOS_DEST'] + '/' + url
            db.session.query(User).filter(User.user_id == user_id).update(dict(profile_picture=profile_picture))
            db.session.commit()

    return redirect('/munchbuddies')


@app.route('/sender_name')
def get_sender_name():
    """Get the current user in session's name."""

    name = session.get('name')

    return name


@app.route('/matches_for_chat.json')
def session_id_for_matches():
    """Returns all the session ids related to the current user."""
    results = get_all_restaurants()
    chat_session_ids = []
    for user_id, restaurant in results.iteritems():
        session_id = query_message_session(user_id)

        if session_id:
            chat_session_ids.append(session_id.sess_id)

    return jsonify(chat_session_ids)


@socketio.on('join', namespace='/munchbuddies')
def join(message):
    room = message['room']
    join_room(room)


@socketio.on('my_room_event', namespace='/munchbuddies')
def send_room_message(message):
    emit('my_response', message, room=message['room'])
    sess = session.get('user_id')
    message_to_db = Message(sess_id=message['room'], from_user_id=sess,
                            to_user_id=message['receiver_id'], message=message['data'])
    db.session.add(message_to_db)
    db.session.commit()


if __name__ == "__main__":
    # set debug to True at the point of invoking the DebugToolbarExtension
    connect_to_db(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "PostgreSQL:///munch"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    
    socketio.run(app, host="0.0.0.0", port=5000)

    # DebugToolbarExtension(app)

    # app.run(host="0.0.0.0")

