from google.appengine.ext import ndb

class UniqueIDEntity(ndb.model):

	model_type = ndb.StringProperty(required=True)

	id = ndb.IntegerProperty(required=True)