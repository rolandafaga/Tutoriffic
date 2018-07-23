from google.appengine.ext import ndb

class UserInfo(ndb.Model):
    nickname = ndb.StringProperty(required=True)
    user_type = ndb.StringProperty()
    sub = ndb.StringProperty()
    availability = ndb.StringProperty()
