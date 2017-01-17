

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import logging
import webapp2

from app.models.playlist_model import PlaylistModel
from app.models.clip_model import ClipModel
from app.models.app_user_model import AppUserModel

from app.util.url_fetch import search_youtube_id

import string
import random

import time
import hashlib
import json

TAG = 'UsersController'


# Changing this will break all current users
SALT_LENGTH = 64


def debug(msg):
	logging.debug(TAG + ' - ' + msg)

# /users
class UsersHandler(webapp2.RequestHandler):
	def get(self):
		user = self.request.get('user')
		
		user_details = AppUserModel.get_users(serialize=True)
		logging.debug(user_details)

		self.response.write(json.dumps(user_details))

# /users/me
class CurrentUserHandler(webapp2.RequestHandler):
	def get(self):
		google_user = users.get_current_user()
		user = AppUserModel.get_user(id=google_user.user_id())
		if user:
			self.response.write(json.dumps(AppUserModel.serialize(user)))
		else:
			self.response.write({})










class GetOtherUsers(webapp2.RequestHandler):

	def get(self):

		user_id = self.request.get('user_id')
		logging.debug(self.request.get('user_id'))
		other_users = AppUserModel.get_users(exclude=user_id, 
			serialize=True)

		self.response.write(json.dumps(other_users))










# /api/v1/login

class LoginHandler(webapp2.RequestHandler):
	
	def post(self):
		
		try:

			payload = json.loads(self.request.body)

			username = payload.get('username')
			password = payload.get('password')

			user = AppUserModel.get_by_username(username)

			salt = user.password[:SALT_LENGTH]

			password = salt + hashlib.sha256(salt + password).hexdigest()

			if password != user.password:
				raise Exception('Invalid password')

			self.response.write(json.dumps(AppUserModel.serialize(user)))
			return
				

		except Exception as e:

			self.error(401)
			self.response.write('Invalid username/password combination')
			return





class RegisterHandler(webapp2.RequestHandler):
	
	def post(self):
		
		try:

			payload = json.loads(self.request.body)

			username = payload.get('username')
			password = payload.get('password')

			rand = random.SystemRandom()
			alphabet = string.ascii_letters + string.digits
			salt = ''.join(rand.choice(alphabet) for i in range(SALT_LENGTH))

			password = salt + hashlib.sha256(salt + password).hexdigest()

			user_key = AppUserModel.register(username=username, password=password)

			if user_key:
				self.response.write(json.dumps(AppUserModel.serialize(user_key.get())))
				return

		except Exception as e:

			self.error(401)
			self.response.write('Error registering user')










# /users/logout
class LogoutHandler(webapp2.RequestHandler):
	def get(self):
		webapp2.redirect(users.create_logout_url('/'))





def get_current_user_id():
	return users.get_current_user().user_id()