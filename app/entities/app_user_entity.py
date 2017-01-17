from google.appengine.ext import ndb

class UserEntity(ndb.Model):

	username = ndb.StringProperty(required=True)

	password = ndb.StringProperty()

	email = ndb.StringProperty()

	google_id = ndb.StringProperty()

	admin = ndb.BooleanProperty(default=False)

	joined = ndb.DateTimeProperty(auto_now=True)