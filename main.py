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
            stuser = UserInfo(user.nickname())
        stuser.put()
        return stuser;
    return None

def get_log_inout_url(user):
    if user:
        return users.create_logout_url('/')
    else:
        return users.create_login_url('/')

class HomeHandler(webapp2.RequestHandler):
    def get(self):

        message = None
        if self.request.get('error'):
            if self.request.get('error') == 'nouser':
                message = 'You must be logged in to do that.'

        user = find_or_create_user()
        log_url = get_log_inout_url(user)

        home_template = jinja_env.get_template('templates/homepage.html')
        self.response.write(home_template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        create_template = jinja_env.get_template('templates/create.html')
        self.response.write(create_template.render())

    def post(self):
        profile_template = jinja_env.get_template('templates/profilepage.html')

        nickname = self.request.get('username')
        user_type = self.request.get('userclass')
        sub = self.request.get('subject')
        availability = self.request.get('avb')


        variables = {
            'nickname': nickname,
            'user_type': user_type,
            'sub': sub,
            'availability': availability,
        }

        info = UserInfo(nickname=nickname, user_type=user_type, sub=sub,
                    availability=availability)
        info.put()

        self.response.write(profile_template.render(variables))

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/create.html')
        self.response.write(home_template.render())

class LogInHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/login.html')
        self.response.write(home_template.render())

class FAQHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/faq.html')
        self.response.write(home_template.render())

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', ProfileHandler),
    ('/signup', SignUpHandler),
    ('/login', LogInHandler),
    ('/faq', FAQHandler)
])
