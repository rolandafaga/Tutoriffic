import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from models import UserInfo

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
@ndb.transactional
def find_or_create_user():
    user = users.get_current_user()
    if user:
        key = ndb.Key('UserInfo', user.user_id())
        stuser = key.get()
        if not stuser:
            stuser = UserInfo(first_name=user.first_name(),
                              last_name=user.last_name())
        stuser.put()
        return stuser;
    return None

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

        info = UserInfo(first_name=first_name, last_name=last_name, user_type=user_type, sub=sub,
                    availability=availability)
        info.put()



app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', ProfileHandler),

])
