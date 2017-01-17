from google.appengine.ext import ndb;

from app.entities.playlist_entity import PlaylistEntity
from app.models.app_user_model import AppUserModel
from app.models.clip_model import ClipModel
from app.libraries.hashids import Hashids
from app.util.errors import *
from app.util.shuffle import get_random_ordering

import logging

import time

from app.libraries.hashids import Hashids

def serialize_time(t):
	t = time.mktime(t.utctimetuple()) * 1000
	t += getattr(t, 'microseconds', 0) / 1000
	return t

class PlaylistModel():

	@staticmethod
	def encode_id(id=None):
		hashids = Hashids(min_length=11)
		return hashids.encode(id)

	@staticmethod
	def decode_id(id=None):
		hashids = Hashids()
		return hashids.decode(id)[0]


	@staticmethod
	def serialize(playlist, fields=None):
		data = {}
		
		if not isinstance(fields, list) or len(fields) == 0:

			data['key'] = playlist.key.urlsafe()

			data['id'] = PlaylistModel.encode_id(playlist.key.id())
		
			data['title'] = playlist.title

			author = playlist.author.get()

			data['author'] = {}
			data['author']['username'] = author.username
			data['author']['email'] = author.email
			data['author']['id'] = author.key.id()

			data['duration'] = playlist.duration

			data['public'] = playlist.public

			data['guests'] = playlist.guests

			data['participants'] = []
			for p in playlist.participants:
				p = p.get()

				participant = {}
				participant['username'] = p.username
				participant['email'] = p.email
				participant['id'] = p.key.id()

				data['participants'].append(participant)

			data['clips'] = []
			logging.debug('ho')
			for clip in playlist.clips:
				clip = ClipModel.serialize(clip.get())

				data['clips'].append(clip)
				logging.debug('hod')
			data['clips'] = [data['clips'][i] for i in get_random_ordering(len(data['clips']))]

		else:

			if 'key' in fields:
				data['key'] = playlist.key.urlsafe()

			if 'title' in fields:
				data['title'] = playlist.title

			if 'author' in fields:

				author = playlist.author.get()

				data['author'] = {}
				data['author']['username'] = author.username
				data['author']['email'] = author.email
				data['author']['id'] = author.key.id()

			if 'duration' in fields:
				data['duration'] = playlist.duration

			if 'public' in fields:
				data['public'] = playlist.public

			if 'guests' in fields:
				data['guests'] = playlist.guests

			if 'participants' in fields:

				data['participants'] = []
				for p in playlist.participants:
					p = p.get()

					participant = {}
					participant['username'] = p.username
					participant['email'] = p.email
					participant['id'] = p.key.id()

					data['participants'].append(participant)

			if 'clips' in fields:
			
				data['clips'] = []
				for clip in playlist.clips:
					clip = ClipModel.serialize(clip.get())

					data['clips'].append(clip)

		return data

	@staticmethod
	def playlist_key():
		return ndb.Key('Playlist', 'Default Playlist Key');

	@staticmethod
	def create_playlist(title=None, author=None, description='', 
		participants=[], users=[], clips=[], tags=[], public=False):

		playlist = PlaylistEntity(
			title=title,
			author=author,
			description='',
			participants=users,
			guests=participants,
			clips=clips,
			tags=tags,
			public=public,
			parent=PlaylistModel.playlist_key())

		

		id = playlist.put().id()
		

		playlist.id = id;

		logging.debug(playlist)

		return playlist.put()


	##### SETTERS ######


	@staticmethod
	def set_title(playlist_key=None, title=None):
		playlist = playlist_key.get()
		if playlist.title == title:
			return False

		playlist.title = title
		playlist.put()
		return True


	@staticmethod
	def set_description(playlist_key=None, description=None):
		playlist = playlist_key.get()
		if playlist.description == description:
			return False

		playlist.description = description
		playlist.put()
		return True


	@staticmethod
	def set_participants(playlist_key=None, participants=[]):
		playlist = playlist_key.get()
		playlist.participants = participants
		playlist.put()
		return True


	@staticmethod
	def set_guests(playlist_key=None, guests=[]):
		playlist = playlist_key.get()
		playlist.guests = guests
		playlist.put()
		return True


	@staticmethod
	def set_public(playlist_key=None, public=False):
		playlist = playlist_key.get()
		playlist.public = public
		return True


	@staticmethod
	def set_tags(playlist_key=None, tags=[]):
		playlist = playlist_key.get()
		playlist.tags = tags
		return True


	@staticmethod
	@ndb.transactional(xg=True, propagation=ndb.TransactionOptions.ALLOWED)
	def set_clips(id=None, clip_keys=None):
		playlist = PlaylistEntity.query(
			PlaylistEntity.id 	== id, 
			ancestor			= PlaylistModel.playlist_key()
		).get()

		for clip_key in playlist.clips:
			
			if clip_key not in clip_keys:
				clip_key.delete()



		playlist.clips = clip_keys
		playlist.put()

		return PlaylistModel.serialize(playlist, fields=['clips'])

	##### GETTERS #####

	@staticmethod
	@ndb.transactional(xg=True, propagation=ndb.TransactionOptions.ALLOWED)
	def add_clips(id=None, clip=None):

		p = PlaylistEntity.query(
			PlaylistEntity.id 	== id, 
			ancestor			= PlaylistModel.playlist_key()
		)

		p = p.get()

		if isinstance(clip, list):
			p.clips.extend(clip)

		else:
			p.clips.append(clip)

		p.put()

		return PlaylistModel.serialize(p, fields=['clips'])

	@staticmethod
	def get_playlists(fields=None):
		query = PlaylistEntity.query(ancestor=PlaylistModel.playlist_key())

		if isinstance(fields, list):
			return query.fetch(fields)
		return  query

	@staticmethod
	def add_participant(playlist_key=None, participant=None):
		playlist = playlist_key.get()

		playlist.participants.append(participant)

		playlist.put()

		return playlist.participants

	@staticmethod
	def get_user_playlists(author_key):
		return PlaylistEntity.query(PlaylistEntity.author==author_key, ancestor=PlaylistModel.playlist_key())


	@staticmethod
	def get_clip_keys(playlist_key=None):
		playlist = playlist_key.get()
		return playlist.clips


	@staticmethod
	def get_clips(playlist=None, serialize=False):
		return [ClipModel.serialize(clip.get()) for clip in playlist.clips]


	@staticmethod
	def add_guest(playlist_key=None, guest=None):
		playlist = playlist_key.get()
		playlist.guests.append(guest)
		playlist.put()


	@staticmethod
	def add_clip(playlist_key=None, clip=None):
		playlist = playlist_key.get()
		playlist.clips.append(clip)
		playlist.put()
		return playlist_key

	@staticmethod
	def get_participants(playlist=None):
		return [AppUserModel.serialize(participant.get()) for participant in playlist.participants]

	@staticmethod
	def delete_clip(playlist_key=None, clip_key=None):
		playlist = playlist_key.get()
		playlist.clips.remove(clip_key)
		clip_key.delete()
		playlist.put()
		return True

	@staticmethod
	@ndb.transactional
	def delete_guest(playlist_key=None, guest=None):
		try:
			playlist = playlist_key.get()
			playlist.guests.remove(guest)
			playlist.put()
			return True

		except Exception as e:
			raise

	@staticmethod
	def add_participant(playlist_key=None, participant=None):
		playlist = playlist_key.get()

		playlist.participants.append(participant)

		playlist.put()

		return playlist.participants

	@staticmethod
	@ndb.transactional
	def delete_participant(playlist_key=None, participant=None):
		try:
			playlist = playlist_key.get()
			logging.debug(playlist)
			playlist.participants.remove(participant)
			playlist.put()
			return True

		except Exception as e:
			raise

	@staticmethod
	def get_by_id(id=None):
		return PlaylistEntity.query(PlaylistEntity.id==id, ancestor=PlaylistModel.playlist_key()).get()


TAG = 'PlaylistModel'

def debug(msg):
	logging.debug(TAG + ' - ' + msg)