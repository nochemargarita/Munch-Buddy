"""Models and database for Munch Buddy project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()

#####################################################################
# Model Definitions


class User(db.Model):
    """User of Munch Buddy Web App."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    display_name = db.Column(db.String(30), nullable=False)
    interests = db.Column(db.String(250), nullable=True)
    profile_picture = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        """Provide a helpful representation."""

        return "<User user_id={} display_name={}>".format(
               self.user_id, self.display_name)


class Category(db.Model):
    """Categories of cuisine."""

    __tablename__ = "categories"

    cat_id = db.Column(db.String(50), nullable=False, primary_key=True)
    cat_title = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide a helpful representation."""
        return "<Category cat_id={} cat_title={}>".format(
               self.cat_id, self.cat_title)

class LikeCategory(db.Model):
    """Restaurants that users liked."""

    __tablename__ = "likes_categories"

    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    cat_id = db.Column(db.String(50), db.ForeignKey("categories.cat_id"), nullable=False)

    # Define relationship to User.
    user = db.relationship("User", backref=db.backref("likes_categories", order_by=like_id))

    # Define ralationship to Category
    category = db.relationship("Category", backref=db.backref("likes_categories", order_by=like_id))

    def __repr__(self):
        """Provide useful representation."""

        return "<LikeCategory like_id={} user_id={} cat_id={}>".format(
               self.like_id, self.user_id, self.cat_id)


class Restaurant(db.Model):
    """Restaurants and their information."""

    __tablename__ = "restaurants"

    rest_id = db.Column(db.String(100), nullable=False, primary_key=True)
    rest_title = db.Column(db.String(100), nullable=False)
    rest_alias = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    num_reviews = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    link = db.Column(db.String(300), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """Provide a helpful representation."""

        return "<Restaurant rest_id={} rest_name={}>".format(
               self.rest_id, self.rest_title.encode('ascii', 'replace'))

class LikeRestaurant(db.Model):
    """Restaurants that user liked."""

    __tablename__ = "likes_restaurants"

    likes_restaurants = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    rest_id = db.Column(db.String(50), db.ForeignKey("restaurants.rest_id"), nullable=False)

    like_restaurant = db.relationship("Restaurant", backref=db.backref("likes_restaurants", order_by=likes_restaurants))

    def __repr__(self):
        """Provide a helpful representation."""

        return "<Like_Restaurant likes_restaurants={} rest_id={}>".format(
                self.likes_restaurants, self.rest_id)


class RestaurantCategory(db.Model):
    """Restaurants and categories."""

    __tablename__ = "restaurants_categories"

    rest_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rest_id = db.Column(db.String(50), db.ForeignKey("restaurants.rest_id"), nullable=False)
    cat_id = db.Column(db.String(50), db.ForeignKey("categories.cat_id"), nullable=False)

    # Define relationship to Restaurant.
    restaurant = db.relationship("Restaurant", backref=db.backref("restaurants_categories", order_by=rest_cat_id))
    # Define relationship to Category.
    category = db.relationship("Category", backref=db.backref("restaurants_categories", order_by=rest_cat_id))

    def __repr__(self):
        """Provide a helpful representation."""

        return "<RestaurantCategory rest_cat_id={} rest_id={} cat_id={}>".format(
               self.rest_cat_id, self.rest_id, self.cat_id)


class Message(db.Model):
    """Users exchange messages."""

    __tablename__ = "messages"

    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sess_id = db.Column(db.Integer, db.ForeignKey("messages_sessions.sess_id"), nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    messaged_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # auto add/fill
    message = db.Column(db.String(300))

    from_user = db.relationship("User", foreign_keys=[from_user_id], backref=db.backref("messages_sent", order_by=message_id))

    to_user = db.relationship("User", foreign_keys=[to_user_id], backref=db.backref("messages_received", order_by=message_id))

    mess_sess = db.relationship("MessageSession", backref=db.backref("messages", order_by=message_id))

    def __repr__(self):
        """Provide useful representation."""

        return "<Message message_id={} from_user_id={} to_user_id={}>".format(
               self.message_id, self.from_user_id, self.to_user_id)


class MessageSession(db.Model):
    """Users unique session id."""

    __tablename__ = "messages_sessions"

    sess_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    def __repr__(self):
        """Provide a helpful representation."""
        return "<MessageSession sess_id={} from_user_id={} to_user_id={}>".format(
                self.sess_id, self.from_user_id, self.to_user_id)



##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///munch'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
    # If module is run interactively,
    # this allows you to work with database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
