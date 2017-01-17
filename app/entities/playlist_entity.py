from google.appengine.ext import ndb;
import time
import logging
class PlaylistEntity(ndb.Model):

	# Playlist title
	title = ndb.StringProperty(required=True)

	# Playlist author
	author = ndb.KeyProperty(required=True)

	# Description of playlist
	description = ndb.StringProperty()

	# Users
	participants = ndb.KeyProperty(repeated=True)

	# Participants (Currently intented for names of unregistered users)
	guests = ndb.StringProperty(repeated=True)

	# Date playlist was created
	created = ndb.DateTimeProperty(auto_now=True)

	# List of video clips
	clips = ndb.KeyProperty(repeated=True)

	# Tags associated with the playlist
	tags = ndb.StringProperty(repeated=True)

	# Public or private playlist
	public = ndb.BooleanProperty(default=False)

	duration = ndb.IntegerProperty(default=60)

	id = ndb.IntegerProperty()

	test = ndb.StringProperty(repeated=True)

	

class ClipsPlaylistsRelationEntity(ndb.Model):

	playlist = ndb.KeyProperty(required=True)

	clip = ndb.KeyProperty(required=True)

	order = ndb.IntegerProperty(required=True)