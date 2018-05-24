from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.security import generate_password_hash, check_password_hash
from model import connect_to_db, db, User, Like, Restaurant, Category, Message, MessageSession, RestaurantCategory
import pearson_algorithm
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room, rooms
from random import choice
# import os
# from datacollector import get_rest_alias_id
# async_mode = None , async_mode=async_mode
app = Flask(__name__)

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


@app.route('/signup')
def signup_form():
    """Directs user to a form."""

    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup():
    """Process signup using post request."""

    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    birthday = request.form.get('birthday')
    interests = request.form.get('interests')

    hashed_password = generate_password_hash(password)
    q = db.session.query(User).filter(User.email == email).first()

    if q:
        flash('Email is already taken.')
        return redirect('/signup')

    else:
        flash('Yay! You are now a Munch Buddy!')
        user = User(email=email, password=hashed_password,
                    fname=fname, lname=lname, birthday=birthday, interests=interests)
        db.session.add(user)
        db.session.commit()
        session['email'] = email
    return redirect('/categories')


@app.route('/login')
def login_form():
    """Directs user to a login form."""
    if 'user_id' in session:
        return redirect('/munchbuddies')
    else:
        return render_template('/login.html')


@app.route('/login', methods=['POST'])
def login():
    """Verify user and log the user in."""

    email = request.form.get('email')
    password = request.form.get('password')
    user = db.session.query(User).filter(User.email == email).first()

    if user:
        checked_hashed = check_password_hash(user.password, password)
        if checked_hashed:
            session['user_id'] = user.user_id
            flash('You successfully logged in.')
            return redirect('/munchbuddies')
        else:
            flash('You have entered the wrong password!')
            return redirect('/login')

    else:
        flash('Please check your email and password!')
        return redirect('/login')


@app.route('/logout')
def logout():
    """Logs the user our from the session."""
    if 'user_id' in session:
        flash('You successfully logged out.')
        session.pop('user_id', None)
        return redirect('/')
    else:
        return render_template('/login.html')
    

@app.route('/categories')
def categories():
    """Let's the user select multiple categories of cuisine."""
    categories = Category.query.all()

    if session.get('email'):
        email = session.pop('email')
        user = db.session.query(User).filter(User.email == email).first()
        session['user_id'] = user.user_id
        return render_template('/categories.html', categories=categories)
    elif session.get('user_id'):
        return render_template('/categories.html', categories=categories)
    else:
        return redirect('/login')


@app.route('/categories', methods=['POST'])
def selected_categories():
    """Get all selected check boxes and add it to database, Like."""

    user = User.query.get(session['user_id'])
    submitted = request.form.getlist('cat_id')

    if submitted:
        for ident in submitted:
            like = Like(user_id=user.user_id, cat_id=ident)

            db.session.add(like)
    db.session.commit()

    return redirect('/munchbuddies')


@app.route('/munchbuddies')
def show_buddies():
    """Directs user to a page with list of people who matched his/her choice of categories."""
    sess = session.get('user_id')

    if sess:
        results = pearson_algorithm.get_all_restaurants(sess)
        matches = {}
        for user_id, restaurant in results.iteritems():
                user = User.query.filter(User.user_id == user_id).first()
                sess_id = MessageSession.query.filter( ((MessageSession.from_user_id == sess) |
                                            (MessageSession.from_user_id == user_id)) &
                                            ((MessageSession.to_user_id == user_id) |  
                                            (MessageSession.to_user_id == sess)) ).first()
                matches[user.user_id] = [user.fname, user.interests, sess_id.sess_id, choice(restaurant)]
                

        pearson_algorithm.create_session(sess)
        return render_template('munchbuddies.html', matches=matches, async_mode=socketio.async_mode)

    else:
        return redirect('/login')




# To receive WebSocket messages from the client the application defines event handlers
# using the socketio.on decorator.

# custom events deliver a JSON payload in a form of python dic
# namespace is an optional argument
# allows client to open multiple connections to the server that are multiplexed in a single socket
# default: attachec to the global namespace
@socketio.on('my_event', namespace='/munchbuddies')
def test_message(message):
    #emit is a function that sends message user a custom event name
    print 'working'
    emit('my_response', {'data': message['data']})

@socketio.on('join', namespace='/munchbuddies')
def join(message):
    join_room(message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.on('my_room_event', namespace='/munchbuddies')
def send_room_message(message):
    emit('my_response', {'data': message['data']}, room=message['room'])


@socketio.on('leave', namespace='/munchbuddies')
def leave(message):
    leave_room(message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.on('disconnect_request', namespace='/munchbuddies')
def disconnect_request():
    emit('my_response',
         {'data': 'Disconnected!'})
    disconnect()

if __name__ == "__main__":
    # set debug to True at the point of invoking the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)

    socketio.run(app, host="0.0.0.0", port=5000)

    # DebugToolbarExtension(app)

    # app.run(host="0.0.0.0")
