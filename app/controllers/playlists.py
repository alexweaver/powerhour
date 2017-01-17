import logging
import webapp2
import json
from app.models.playlist_model import PlaylistModel
from app.models.app_user_model import AppUserModel
from app.models.clip_model import ClipModel
from google.appengine.ext import ndb
from google.appengine.api import users
from app.libraries.hashids import Hashids

from google.appengine.api import taskqueue

from app.entities.playlist_entity import PlaylistEntity
from app.entities.playlist_entity import ClipsPlaylistsRelationEntity
import threading
from app.util.url_fetch import get_details
import time

import re


# /playlists<:/?>
# /playlists/<key><:/?>

class PlaylistsHandler(webapp2.RequestHandler):

	def get(self, playlist_id):
		logging.debug(playlist_id)
		if isinstance(playlist_id, basestring) and playlist_id != '' and playlist_id != '/':

			hashids = Hashids()
			playlist_id = hashids.decode(playlist_id)[0]
			logging.debug(playlist_id)
			try:
				playlist = PlaylistModel.get_by_id(playlist_id)
			except:
				raise Exception('Resource not found, id is of type ' + type(playlist_id).__name__ + ' and is ' + str(playlist_id))

			fields = self.request.get_all('fields')
			if not isinstance(fields, list) or len(fields) == 0:
				fields = None
			logging.debug('hey')
			playlist = PlaylistModel.serialize(
				playlist=playlist, 
				fields=fields)

			logging.debug(playlist)
			self.response.write(json.dumps(playlist))

			return

		playlists = PlaylistModel.get_playlists()
		playlists = [PlaylistModel.serialize(playlist) for playlist in playlists]
		self.response.write(json.dumps(playlists))

		return





	def post(self, playlist_id):

		try:

			logging.debug('Creating New Playlist')

			# If key provided, throw exception
			if isinstance(playlist_id, basestring) and playlist_id != '' and playlist_id != '/':
				raise Exception('Attempting to create playlist with duplicate key')

			# Get request payloads
			payload = json.loads(self.request.body)

			# Get title
			title = payload.get('title')
			if not isinstance(title, basestring):
				raise Exception

			# Get author ID
			author = long(payload.get('author'))
			if not isinstance(author, long):
				raise Exception

			# Get author key from id
			author = AppUserModel.get_by_id(author).key

			# Create playlist
			playlist_key = PlaylistModel.create_playlist(author=author, title=title)

			playlist = playlist_key.get()
			
			PlaylistModel.add_participant(playlist_key=playlist_key, participant=author)

			self.response.write(json.dumps(PlaylistModel.serialize(playlist_key.get())))

			return

		# Catch exceptions
		except Exception as e:

			# Rethrow exception
			raise



	def put(self, playlist_id):


		logging.debug(playlist_id)
		hashids = Hashids(min_length=11)

		playlist_id = hashids.decode(playlist_id)[0]
		playlist = PlaylistModel.get_by_id(playlist_id)

		logging.debug('Saving Playlist')
		logging.debug('Playlist key: ' + str(playlist_id))

		playlist_key = playlist.key

		logging.debug(payload)

		#####	BEGIN MASSIVE VALIDATION LOGIC	#####

		#	Schema:
		#
		#		playlist_key (string) (required)
		#		title (string) (required)
		#		description (string) (required)
		# 		guests (array[string]) (required)
		#		tags (array[string]) (required)
		#		public (boolean) (required)

		title = payload.get('title')
		if not isinstance(title, basestring):
			raise Exception

		author = long(payload.get('author'))
		if not isinstance(author, long):
			raise Exception

		description = payload.get('description')
		if not isinstance(description, basestring):
			raise Exception

		participants = payload.get('participants')
		if not isinstance(participants, list):
			raise Exception

		for participant in participants:
			participant = long(participant)
			if not isinstance(participant, long):
				raise Exception

		tags = payload.get('tags')
		if not isinstance(tags, list):
			raise Exception

		for tag in tags:
			if not isinstance(tag, str):
				raise Exception

		public = payload.get('public')
		if not isinstance(public, bool):
			raise Exception

		clips = payload.get('clips')
		if not isinstance(clips, list):
			raise Exception

		for clip in clips:
			if not isinstance(clip, dict):
				raise Exception

			owned = clip.get('owned')
			if not isinstance(owned, bool):
				raise Exception

			if owned:
				owner = long(clip.get('owner'))
				if not isinstance(owner, long):
					raise Exception

			else:
				guest = clip.get('guest')
				if not isinstance(guest, basestring):
					raise Exception

			start_seconds = int(clip.get('start_seconds'))
			if not isinstance(start_seconds, int):
				raise Exception

			end_seconds = int(clip.get('end_seconds'))
			if not isinstance(end_seconds, int):
				raise Exception

			vid = clip.get('vid')
			if not isinstance(vid, basestring):
				raise Exception





		#####	END MASSIVE VALIDATION LOGIC	#####




		PlaylistModel.set_title(playlist_key, title)

		PlaylistModel.set_description(playlist_key, description)

		participants = [AppUserModel.get_by_id(long(participant)).key for participant in participants]
		PlaylistModel.set_participants(playlist_key, participants)

		request_clips = clips
		clips = []

		for request_clip in request_clips:

			clip_key = ClipModel.save_clip(key=request_clip.get('key'),
				vid=request_clip.get('vid'),
				start_seconds=request_clip.get('start_seconds'),
				end_seconds=request_clip.get('end_seconds'),
				owner=long(request_clip.get('owner')),
				owned=True,
				creator=AppUserModel.get_by_id(author).key,
				create=True)

			clips.append(clip_key)

		PlaylistModel.set_clips(playlist_key, clips)

		PlaylistModel.set_tags(playlist_key, tags)

		PlaylistModel.set_public(playlist_key, public)

		self.response.write(json.dumps(PlaylistModel.serialize(playlist_key.get())))





class GetPlaylistList(webapp2.RequestHandler):
	def get(self):
		playlists = PlaylistModel.get_playlists()
		playlists = [PlaylistModel.serialize(playlist) for playlist in playlists]
		self.response.write(json.dumps(playlists))















# /api/v1/playlists/<playlist_id>/title

class PlaylistsTitleHandler(webapp2.RequestHandler):




	# Get playlist title

	def get(self, playlist_id):

		try: # Attempt get request

			# Validate mix id
			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Mix id not provided or of wrong type')

			# Get entity id from client id
			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)

			# Return playlist title
			self.response.write(json.dumps(playlist.title))

			return # End request

		# Catch exception
		except Exception as e:

			# Rethrow exception
			raise Exception(e)





	# Set playlist title

	def put(self, playlist_id):

		try: # Attempt put request

			# Validate mix id
			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Mix id not provided or of wrong type')

			# Get entity id from client id
			playlist_id = PlaylistModel.decode_id(playlist_id)

			# Get playlist
			playlist = PlaylistModel.get_by_id(playlist_id)

			# Get payload
			payload = json.loads(self.request.body)

			# Get title from request
			title = payload.get('title')
			if not isinstance(title, basestring):
				raise Exception('Title not provided or not basestring')

			logging.debug(payload)

			PlaylistModel.set_title(playlist.key, title)

			# Return playlist title
			self.response.write(json.dumps({'title': playlist.title}))

			return # End request

		# Catch exception
		except Exception as e:

			# Rethrow exception
			raise Exception(e)	









# /playlists/<playlist_id>/participants<:/?>

class PlaylistsParticipantsHandler(webapp2.RequestHandler):




	# Get playlist participants
	def get(self, playlist_id):

		try:

			# Validate mix id
			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Mix id not provided or of wrong type')
			
			# Get entity id from client id
			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)

			data = PlaylistModel.serialize(playlist, fields=['participants'])

			self.response.write(json.dumps(data))

			return

		except Exception as e:

			raise Exception(e)





	# Add playlist participant		
	def post(self, playlist_id):

		try:

			# Validate mix id
			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Mix id not provided or of wrong type')

			# Get entity id from client id
			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)

			payload = json.loads(self.request.body)

			participant = long(payload.get('participant'))
			if not isinstance(participant, long):
				raise Exception('Participant not provided or not long')

			participant = AppUserModel.get_by_id(participant).key

			PlaylistModel.add_participant(playlist.key, participant)

			data = PlaylistModel.serialize(playlist, fields=['participants'])

			self.response.write(json.dumps(data))

			return

		except Exception as e:

			raise Exception(e)





	# Delete playlist participant
	def delete(self, playlist_id):
		try:
			
			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Invalid playlist id')


			participant = long(self.request.get('participant'))
			if not isinstance(participant, long):
				raise Exception('Invalid participant id')

			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)

			participant = AppUserModel.get_by_id(participant)

			PlaylistModel.delete_participant(playlist.key, participant.key)


		except Exception as e:
			raise










# /playlists/<playlist_id>/guests<:/?>

class PlaylistsGuestsHandler(webapp2.RequestHandler):





	# Get playlist guests
	def get(self, playlist_id):

		try:

			# Validate mix id
			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Mix id not provided or of wrong type')

			# Get entity id from client id
			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)

			# Respond with updated guests
			self.response.write(json.dumps(playlist.guests))

			return

		# Catche exceptions
		except Exception as e:

			raise Exception(e)

			



	# Add guest to playlist
	def post(self, playlist_id):

		try:

			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Mix id invalid type or empty')

			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)

			payload = json.loads(self.request.body)

			guest = payload.get('guest')
			if not isinstance(guest, basestring):
				raise Exception('Guest not provided or not basestring')

			PlaylistModel.add_guest(playlist.key, guest)

			self.response.write(json.dumps(playlist.guests))

		except Exception as e:
			raise




	def delete(self, playlist_id):
		try:
			playlist_id = playlist_id
			
			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Invalid playlist id')


			guest = self.request.get('guest')
			if not isinstance(guest, basestring):
				raise Exception('Invalid guest')


			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)


			logging.debug(self.request.get('guest'))


			PlaylistModel.delete_guest(playlist.key, guest)


		except Exception as e:
			raise










# /api/v1/<playlist_id>/clips<:/>

class PlaylistsClipsHandler(webapp2.RequestHandler):


	def get(self, playlist_id):

		try:

			# Validate mix id
			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Mix id not provided or of wrong type')

			# Get entity id from client id
			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)

			# Respond with updated guests
			self.response.write(json.dumps(PlaylistModel.serialize(playlist=playlist, fields=['clips'])))

			return

		# Catche exceptions
		except Exception as e:

			raise Exception(e)





	# Add playlist clip
	def post(self, playlist_id):
		logging.debug('add clips')
		try:

			if not isinstance(playlist_id, basestring) or playlist_id == '':
				raise Exception('Mix id invalid type or empty')

			playlist_id = PlaylistModel.decode_id(playlist_id)
			playlist = PlaylistModel.get_by_id(playlist_id)

			payload = json.loads(self.request.body)

			clips = payload['clips']

			clips = clips if isinstance(clips, list) else [clips]

			keys = []

			for clip in clips:
				if not isinstance(clip, dict):
					raise Exception('Clip not object')

				participant = clip['participant'] if 'participant' in clip else None
				participant = AppUserModel.get_by_id(participant).key if participant is not None else None

				guest = clip['guest'] if 'guest' in clip else None

				# Set start seconds for clip
				start_seconds = clip['start'] if 'start' in clip else None

				# Set end seconds for clip
				end_seconds = clip['end'] if 'end' in clip else None

				# Set vid for clip
				vid = clip['vid'] if 'vid' in clip else None
				 
				details = get_details(vid)

				# duration = details['duration']

				# hours = re.search('[0-9]{1,2}H', duration)
				# hours = int(hours.group()[:-1]) if hours is not None else 0

				# minutes = int(re.search('[0-9]{1,2}M', duration).group()[:-1])
				# seconds = int(re.search('[0-9]{1,2}S', duration).group()[:-1])

				# duration = hours * 3600 + minutes * 60 + seconds

				# logging.debug(duration)
				# logging.debug((hours, minutes, seconds))

				creator = long(clip['creator']) if 'creator' in clip else None
				creator = AppUserModel.get_by_id(creator).key

				
				clip = ClipModel.create_clip(
					vid 			= vid,
					start_seconds	= start_seconds,
					end_seconds		= end_seconds,
					participant 	= participant,
					guest			= guest,
					creator 		= creator
				)

				logging.debug(clip)
				keys.append(clip)

			logging.debug(keys)
			self.response.write(json.dumps(PlaylistModel.set_clips(playlist_id, keys)))

			return 

		except Exception:

		 	raise
