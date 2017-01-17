from google.appengine.ext import ndb;

from app.entities.clip_entity import ClipEntity
from app.models.app_user_model import AppUserModel
from app.util.url_fetch import get_details
from app.util.url_fetch import get_snippet

import logging



import time
from google.appengine.api import memcache

class ClipModel():

	@staticmethod
	def clip_key():
		return ndb.Key('Clip', 'Default Clip Key')





	@staticmethod
	def serialize(clip, fields=None):
		data = {}

		if not isinstance(fields, list):
			
			data['key'] = clip.key.urlsafe()

			data['vid'] = clip.vid

			data['start_seconds'] = clip.start_seconds

			data['end_seconds'] = clip.end_seconds

			if clip.participant is not None:

				participant = clip.participant.get()

				data['participant'] 				= {}
				data['participant']['username'] 	= participant.username
				data['participant']['id'] 			= participant.key.id()

			elif clip.guest is not None:

				data['guest'] = {}
				data['guest']['username'] = clip.guest

			creator = clip.creator.get()

			data['creator'] 			= {}
			data['creator']['username'] = creator.username
			data['creator']['id'] 		= creator.key.id()
			
			data['created'] = serialize_time(clip.created)

			snippet = get_snippet(data['vid'])
			details = get_details(data['vid'])

			data['duration'] = details.get('duration')
			
			data['title'] = snippet.get('title')

		return data





	@staticmethod
	def create_clip(vid, start_seconds, end_seconds, participant, guest=None, creator=None):

		logging.debug(creator)
		clip = ClipEntity(vid=vid, 
					start_seconds=start_seconds, 
					end_seconds=end_seconds,
					participant=participant,
					guest=guest,
					creator=creator, 
					parent=ClipModel.clip_key())

		return clip.put()

	@staticmethod
	def save_clip(key=None, vid=None, start_seconds=None, end_seconds=None,
		participant=None, guest=None, creator=None, create=False):

		if isinstance(key, basestring):
			key = ndb.Key(urlsafe=key)
			clip = key.get()

			if isinstance(vid, basestring):
				clip.vid = vid

			if isinstance(int(start_seconds), int):
				clip.start_seconds = int(start_seconds)

			if isinstance(int(end_seconds), int):
				clip.end_seconds = int(end_seconds)

			elif isinstance(guest, basestring) and clip.owner is None:
				clip.guest = guest

			return clip.put()

		elif create:
			clip_key = None
			if isinstance(owner, long) and guest is None:
				clip_key = ClipModel.create_clip(vid=vid,
					start_seconds=start_seconds,
					end_seconds=end_seconds,
					participant=AppUserModel.get_by_id(owner).key,
					guest=guest,
					creator=creator)
			elif isinstance(guest, basestring) and owner is None:
				clip_key = ClipModel.create_clip(vid=vid,
					start_seconds=start_seconds,
					end_seconds=end_seconds,
					participant=participant,
					guest=guest,
					creator=creator)
			return clip_key

		return False

	@staticmethod
	def edit_clip_time(clip_key, start_seconds, end_seconds):
		logging.debug('Editing clip start seconds')

		clip = clip_key.get()

		clip.start_seconds = start_seconds
		clip.end_seconds = end_seconds

		return clip.put().get()

def serialize_time(t):
	t = time.mktime(t.utctimetuple()) * 1000
	t += getattr(t, 'microseconds', 0) / 1000
	return t