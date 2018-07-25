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

def check_user():
    user = users.get_current_user()
    if not user:
        return None
    else:
        key = ndb.Key('UserInfo', user.user_id())
        stuser = key.get()
        if not stuser:
            stuser = UserInfo(key=key,
                          name=user.nickname(),
                          email=user.email(),
                          page_count=0)
        stuser.page_count += 1
        stuser.put()
        return stuser;

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/homepage.html')
        user = check_user()
        if not user:
            variables = {
                'login_button': 'show',
                'logout_button': 'hide',
                'url': users.create_login_url('/create')
            }
        else:
            variables = {
                'login_button': 'hide',
                'logout_button': 'show',
                'url': users.create_logout_url('/')
            }
        self.response.write(home_template.render(variables))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        create_template = jinja_env.get_template('templates/create.html')
        user = check_user()
        if not user:
            self.redirect(users.create_login_url('/create'))

        variables = {
            'login_button': 'hide',
            'logout_button': 'show',
            'url': users.create_logout_url('/'),
        }
        self.response.write(create_template.render(variables))


    def post(self):
        print("boi")
        search_template = jinja_env.get_template('templates/create.html')

        user_type = self.request.get('userclass')
        sub = self.request.get('subject')
        availability = self.request.get('avb')
        user = users.get_current_user()
        user_id = user.user_id()
        name = user.nickname()


        variables = {
            'name': name,
            'user_type': user_type,
            'sub': sub,
            'availability': availability,
            'user_id': user_id,
        }
        print(variables)
        info = SearchForm(name=name, user_type=user_type, sub=sub,
                    avb=availability, id=user_id)
        info.put()
        print(search_template)

        self.redirect('/list')

class ListHandler(webapp2.RequestHandler):
    def get(self):
        list_template = jinja_env.get_template('templates/list.html')
        tutors = SearchForm.query(SearchForm.user_type == "tutor").fetch()
        variables = {
            'clients': tutors,
        }
        self.response.write(list_template.render(variables))

class FAQHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/faq.html')
        user = check_user()
        if not user:
            variables = {
                'login_button': 'show',
                'logout_button': 'hide',
                'url': users.create_login_url('/create')

            }
        else:
            variables = {
                'login_button': 'hide',
                'logout_button': 'show',
                'url': users.create_logout_url('/'),
            }
        self.response.write(home_template.render(variables))

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', ProfileHandler),
    ('/faq', FAQHandler),
    ('/list', ListHandler)
], debug=True)
