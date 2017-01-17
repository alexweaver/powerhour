from google.appengine.ext import ndb;

class ClipEntity(ndb.Model):

	# Id of the clip video
	vid = ndb.StringProperty(required=True)

	# Seconds mark to start clip
	start_seconds = ndb.IntegerProperty(required=True)

	# Seconds mark to end clip
	end_seconds = ndb.IntegerProperty(required=True)

	# Whether or not this clip is owned
	participant = ndb.KeyProperty()

	# Participant
	guest = ndb.StringProperty()

	# Creator of the clip
	creator = ndb.KeyProperty(required=True)

	# Date clip was created
	created = ndb.DateTimeProperty(auto_now=True)