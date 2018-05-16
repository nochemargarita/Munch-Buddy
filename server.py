from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.security import generate_password_hash, check_password_hash
from model import connect_to_db, db, User, Like , Restaurant, Category, Message, RestaurantCategory
import os
# from datacollector import get_rest_alias_id
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Homepage."""

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

    hashed_password = generate_password_hash(password)
    q = db.session.query(User).filter(User.email == email).first()

    if q:
        flash('Email is already taken.')
        return redirect('/signup')

    else:
        flash('Yay! You are now a Munch Buddy!')
        session['email'] = email
        user = User(email=email, password=hashed_password,
                    fname=fname, lname=lname, birthday=birthday)
        db.session.add(user)
        db.session.commit()
        return redirect('/categories')

@app.route('/login')
def login_form():
    """Directs user to a login form."""

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
            return redirect('/')

    else:
        flash('Please check your email and password!')
        return redirect('/login')


@app.route('/logout')
def logout():
    """Logs the user our from the session."""
    flash('You successfully logged out.')
    session.pop('email', None)
    return redirect('/')


@app.route('/categories')
def categories():
    """Let's the user select multiple categories of cuisine."""
    categories = Category.query.all()
    if session.get('email'):
        return render_template('/categories.html', categories=categories)
    else:
        return redirect('/login')

@app.route('/categories', methods=['POST'])
def selected_categories():
    """Get all selected check boxes and add it to database Like."""

    categories = Category.query.all()

    user = User.query.get(session['user_id'])

    for cat_id in range(1, len(categories) + 1):
        submitted = request.form.get('{}'.format(cat_id))
        if submitted:
            like = Like(user_id=user_id.user_id, cat_id=cat_id)

            db.session.add(like)

            for category in categories:
                if category.cat_id == cat_id:
                    for restaurant in get_rest_alias_id():
                        if category.cat_alias in restaurant:
                            rest_cat = RestaurantCategory(rest_id=restaurant[1], cat_id=cat_id )

                            db.session.add(rest_cat)
    db.session.commit()

    return redirect('/')



@app.route('/munchbuddies')
def show_buddies():
    """Directs user to a page of people who matched his/her choice of categories."""

    pass

if __name__ == "__main__":
    # set debug to True at the point of invoking the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
