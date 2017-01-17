from google.appengine.ext import ndb;

class PermissionEntity(ndb.Model):

	user = ndb.UserProperty(required=True)

	subject = ndb.KeyProperty(required=True)

	admin = ndb.BooleanProperty(required=True, default=False)

	edit = ndb.BooleanProperty(required=True, default=False)

	view = ndb.BooleanProperty(required=True, default=False)

	created = ndb.DateTimeProperty(auto_now=True)