import webapp2
import jinja2
import os
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class LoginHandler(webapp2.RequestHandler):
    
