import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from models import UserInfo

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
        print("boi")
        profile_template = jinja_env.get_template('templates/profilepage.html')

        first_name = self.request.get('fname')
        last_name = self.request.get('lname')
        nickname = self.request.get('username')
        user_type = self.request.get('userclass')
        sub = self.request.get('subject')
        availability = self.request.get('avb')


        variables = {
            'first_name': first_name,
            'last_name': last_name,
            'nickname': nickname,
            'user_type': user_type,
            'sub': sub,
            'availability': availability,
        }
        print(variables)
        info = UserInfo(nickname=nickname, user_type=user_type, sub=sub,
                    availability=availability)
        info.put()
        print(profile_template)

        self.response.write(profile_template.render(variables))

class StudentProfile(webapp2.RequestHandler):
    def get(self):
        sprofile_template = jinja_env.get_template('templates/studentprofilepage.html')
        self.response.write(sprofile_template.render())

class LogInHandler(webapp2.RequestHandler):
    def get(self):
        login_template = jinja_env.get_template('templates/login.html')

        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            url = users.create_logout_url('/login')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, url)
            variables = {'user': user,
                         'url': url
                         }
        else:
            url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(url)
            variables = {'user': user,
                         'url': url
                         }

        self.response.write(login_template.render(variables))

class FAQHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/faq.html')
        self.response.write(home_template.render())

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', ProfileHandler),
    ('/sprofile', StudentProfile),
    ('/login', LogInHandler),
    ('/faq', FAQHandler)
], debug=True)
