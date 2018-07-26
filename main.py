import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from models import UserInfo
from models import SearchForm
from google.appengine.api import mail


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
        email = user.email()


        variables = {
            'name': name,
            'user_type': user_type,
            'sub': sub,
            'availability': availability,
            'user_id': user_id,
            'email': email,
        }
        print(variables)
        info = SearchForm(name=name, user_type=user_type, sub=sub,
                    avb=availability, id=user_id, email=email)
        existing_info = SearchForm.query(SearchForm.name == name,
                                         SearchForm.email == email,
                                         SearchForm.sub == sub,
                                         SearchForm.id == user_id,
                                         SearchForm.avb == availability,
                                         SearchForm.user_type == user_type).fetch(limit = 1)
        if len(existing_info) > 0:
            self.redirect('/list?id=%s'% existing_info[0].key.urlsafe())
        else:
            info.put()
            self.redirect('/list?id=%s'% info.key.urlsafe())

class ListHandler(webapp2.RequestHandler):
    def get(self):
        list_template = jinja_env.get_template('templates/list.html')
        id = self.request.get('id')
        key = ndb.Key(urlsafe=id)
        temp_name = key.get()
        if not temp_name:
            self.error(404)
            self.response.out.write('Page not found')
            return

        tutors = SearchForm.query(SearchForm.user_type != temp_name.user_type,
                                  SearchForm.sub == temp_name.sub,
                                  SearchForm.avb == temp_name.avb).fetch()

        user = check_user()
        if not user:
            variables = {
                'login_button': 'show',
                'logout_button': 'hide',
                'url': users.create_login_url('/create'),
                'clients': tutors,
            }
        else:
            variables = {
                'login_button': 'hide',
                'logout_button': 'show',
                'url': users.create_logout_url('/'),
                'clients': tutors,
            }
        self.response.write(list_template.render(variables))
    def post(self):
        print("@@@@###$$$")
        print(self.request.get('email'))
        print("Hello!")
        id = self.request.get('id')
        key = ndb.Key(urlsafe=id)
        temp_name = key.get()
        sender = temp_name.email
        sender_name = temp_name.name
        receiver_mail = self.request.get('email')
        receiver_name = self.request.get('name')
        subject = "A Tutoriffic user messaged you!"
        body = self.request.get('body')

        mail.send_mail(sender, receiver_mail, subject, body)

        self.redirect('/')



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
