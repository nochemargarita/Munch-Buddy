from unittest import TestCase
from model import connect_to_db, db, seed, 
from server import app
from flask import session

import unittest

from server import app
from model import db, seed_data, connect_to_db, User

import server
import flask

from StringIO import StringIO  

connect_to_db(app)

class FlaskTestsHome(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "PostgreSQL:///munch"

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Munch Buddy", result.data)


class FlaskTestsSignup(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "PostgreSQL:///munch"

    def test_index(self):
        """Test sign up page."""

        result = self.client.get("/")
        self.assertIn("Interests", result.data)
        self.assertNotIn("Saved Restaurants", result.data)
        self.assertNotIn("Log out", result.data)


# class FlaskTestsLogin(TestCase):
#     """Flask tests."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()

#         # Show Flask errors that happen during tests
#         app.config['TESTING'] = True
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#         app.config["SQLALCHEMY_DATABASE_URI"] = "PostgreSQL:///munch"

#     def test_index(self):
#         """Test log in page."""

#         result = self.client.get("/")
#         self.assertIn("Email", result.data)


# class FlaskTestsCategories(TestCase):
#     """Flask tests."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()

#         # Show Flask errors that happen during tests
#         app.config['TESTING'] = True
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#         app.config["SQLALCHEMY_DATABASE_URI"] = "PostgreSQL:///munch"


#     def test_index(self):
#         """Test categories page."""
        
#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = '1'

        
#         result = self.client.post("/categories")

        # print result.data



        
# class FlaskTestsDatabase(TestCase):
#     """Flask tests that use the database."""

# #     def setUp(self):
# #         """Stuff to do before every test."""

# #         # Get the Flask test client
# #         self.client = app.test_client()
# #         app.config['TESTING'] = True

# #         # Connect to test database
# #         connect_to_db(app, "postgresql:///exampledata")

# #         # Create tables and add sample data
# #         db.create_all()
# #         example_data()

# #     def tearDown(self):
# #         """Do at end of every test."""

# #         db.session.close()
# #         db.drop_all()

#     def test_categories_list(self):
#         """Test departments page."""

#         result = self.client.get("/departments")
#         self.assertIn("Legal", result.data)

#     def test_departments_details(self):
#         """Test departments page."""

#         result = self.client.get("/department/fin")
#         self.assertIn("Phone: 555-1000", result.data)

#     def test_login(self):
#         """Test login page."""

#         result = self.client.post("/login",
#                                   data={"user_id": "rachel", "password": "123"},
#                                   follow_redirects=True)
#         self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_important_page(self):
#         """Test log in page."""

#         result = self.client.get("/login", follow_redirects=True)
#         self.assertIn("Munch", result.data)
#         # self.assertIn("You successfully logged in.", result.data)
#         # self.assertNotIn("Sign Up", result.data)



# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/logout", follow_redirects=True)
#         self.assertNotIn("email", result.data)
#         self.assertIn("Sign Up", result.data)
#         self.assertIn("You successfully logged out.", result.data)


# class FlaskTestsLogInLogOut(TestCase):
#     """Test log in and log out."""

#     def setUp(self):
#         """Before every test"""

#         app.config['TESTING'] = False
#         self.client = app.test_client()

#     def test_login(self):
#         """Test log in form."""

#         with self.client as c:
          
#             result = c.post('/login',
#                             data={'user_id': 1},
#                             follow_redirects=True)

#             self.assertEqual(session['user_id'], 1)
            # self.assertIn("You are a valued user", result.data)

 

    # def test_logout(self):
    #     """Test logout route."""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess['user_id'] = 1

    #         result = self.client.get('/logout', follow_redirects=True)

    #         self.assertNotIn('user_id', session)
    #         self.assertIn('logged out', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
