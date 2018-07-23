import webapp2
import jinja2
import os
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
        profile_info = self.request.get('create')



app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', ProfileHandler),

])
