import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from models import UserInfo
from models import SearchForm

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
        search_template = jinja_env.get_template('templates/create.html')

        user_type = self.request.get('userclass')
        sub = self.request.get('subject')
        availability = self.request.get('avb')
        user = users.get_current_user()
        user_id = user.user_id()


        variables = {
            'name': user.nickname(),
            'user_type': user_type,
            'sub': sub,
            'availability': availability,
            'user_id': user_id
        }
        print(variables)
        info = SearchForm(name=name, user_type=user_type, sub=sub,
                    avb=availability, id=user_id)
        info.put()
        print(search_template)

        self.response.write(search_template.render(variables))

class StudentProfile(webapp2.RequestHandler):
    def get(self):
        sprofile_template = jinja_env.get_template('templates/studentprofilepage.html')
        self.response.write(sprofile_template.render())

class LogInHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if not user:
            loggedout_template = jinja_env.get_template('templates/login.html')
            values = {
                'url': users.create_login_url('/create')
            }
            self.response.write(loggedout_template.render(values))
        else:
            key = ndb.Key('UserInfo', user.user_id())
            my_visitor = key.get()
            if not my_visitor:
                my_visitor = UserInfo(key=key,
                                    name=user.nickname(),
                                    email=user.email(),
                                    id=user.user_id(),
                                    page_count=0)
            my_visitor.page_count += 1
            my_visitor.put()

            loggedin_template = jinja_env.get_template('templates/create.html')
            values = {
                'url': users.create_logout_url('/'),
                'name': user.nickname(),
                'email': user.email(),
                'user_id': user.user_id(),
                'view_number': my_visitor.page_count
            }

            self.response.write(loggedin_template.render(values))

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
