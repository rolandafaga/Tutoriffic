import webapp2
import jinja2
import os
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
class Info(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    user_password = ndb.StringProperty(required=True)
    user_type = ndb.StringProperty(required=True)
    sub = ndb.StringProperty(required=True)
    availability = ndb.StringProperty(required=True)
    
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
        email = self.request.get('usermail')
        user_password = self.request.get('password')
        user_type = self.request.get('userclass')
        sub = self.request.get('subject')
        availability = self.request.get('avb')


        variables = {
            ''
        }



app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', ProfileHandler),

])
