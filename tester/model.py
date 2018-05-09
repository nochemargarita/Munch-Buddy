"""Models and database for Munch Buddy project."""

from flask_sqlalchemy import SQLAlchemy


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
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        """Provide a helpful representation."""

        return "<User user_id={} email={} fname={} lname={} birthday={}>".format(
                self.user_id, self.email, self.fname, self.lname, self.birthday)


class Like(db.Model):
    """Restaurants that users liked."""

    __tablename__ = "likes"

    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    rest_id = db.Column(db.Integer, db.ForeignKey("restaurants.rest_id"), nullable=False)

    # Define relationship to User.
    user = db.relationship("User", backref=db.backref("likes", order_by=like_id))

    # Define ralationship to Restaurant
    restaurant = db.relationship("Restaurant", backref=db.backref("likes", order_by=like_id))

    def __repr__(self):
        """Provide useful representation."""

        return "<Like like_id={} user_id={} rest_id={}>".format(
                self.like_id, self.user_id, self.rest_id)


class Category(db.Model):
    """Categories of cuisine."""

    __tablename__ = "categories"

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cat_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide a helpful representation."""
        return "<Category cat_id={} cat_name={}>".format(
                    self.cat_id, self.cat_name)

class Restaurant(db.Model):
    """Restaurants and their information."""

    __tablename__ = "restaurants"

    rest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rest_name = db.Column(db.String(50), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey("categories.cat_id"), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    # Define relationship to Category.
    category = db.relationship("Category", backref=db.backref("restaurants", order_by=rest_id))

    def __repr__(self):
        """Provide a helpful representation."""

        return "<Restaurant rest_id={} rest_name={}>".format(
                    self.rest_id, self.rest_name)

class Comment(db.Model):
    """Users exchange messages."""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    commented_on = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(250))

    # Define relationship to User.
    # can you use 2 foreign keys from the same table?

    from_user = db.relationship("User", foreign_keys=[from_user_id], backref=db.backref("comments_sent", order_by=comment_id))

    to_user = db.relationship("User", foreign_keys=[to_user_id], backref=db.backref("comments_received", order_by=comment_id))
# figure out how to connect 2 users later.
# A user can have many messages
# Conversation table

    def __repr__(self):
        """Provide useful representation."""

        return "<Comment comment_id={} from_user_id={} to_user_id={}>".format(
                self.comment_id, self.from_user_id, self.to_user_id)

# INSERT INTO users (email, password, fname, lname, birthday)
# VALUES ('noch@yahoo.com', '12345', 'Mar', 'Noc', 'March 25, 1980' );


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    # configure to user PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "PostgreSQL:///munch"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(
        app)


if __name__ == "__main__":
    # If module is run interactively,
    # this allows you to work with database directly.

    from server import app
    connect_to_db(app)
    print "Connected tp DB."
