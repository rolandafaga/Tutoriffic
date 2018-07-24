from google.appengine.ext import ndb

class UserInfo(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    id = ndb.StringProperty(required=True)
    page_count = ndb.IntegerProperty(required=True)

class SearchForm(ndb.Model):
    sub = ndb.StringProperty(required=True)
    user_type = ndb.StringProperty(required=True)
    avb = ndb.StringProperty(required=True)
    id = ndb.StringProperty(required=True)
