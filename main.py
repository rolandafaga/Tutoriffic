import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/homepage.html')
        self.response.write(home_template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        create_template = jinja_env.get_template('templates/create.html')
        self.response.write(create_template.render())

    def post(self):
        profile_template = jinja_env.get_template('templates/profilepage.html')

        first_name = self.request.get('fname')
        last_name = self.request.get('lname')
        user_type = self.request.get('userclass')
        sub = self.request.get('subject')
        availability = self.request.get('avb')


        variables = {
            'first_name': first_name,
            'last_name': last_name,
            'user_type': user_type,
            'sub': sub,
            'availability': availability,
        }

        info = UserInfo(first_name=first_name, last_name=last_name, email=email,
                    user_password=user_password, user_type=user_type, sub=sub,
                    availability=availability)
        info.put



app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', ProfileHandler),

])
