from google.appengine.ext import ndb
from google.appengine.api import users

from app.entities.app_user_entity import UserEntity

import logging
import time
import json

class AppUserModel():

	@staticmethod
	def user_key():
		return ndb.Key('User', 'Default User Key');

	@staticmethod
	def serialize(user):
		data = {}

		data['username'] = user.username
		data['email'] = user.email
		data['google_id'] = user.google_id
		data['joined'] = serialize_time(user.joined)
		data['key'] = user.key.urlsafe()
		data['id'] = user.key.id()
		
		return data

	@staticmethod
	def register(username=None, google_id=None, email=None, password=None, admin=False):

		if AppUserModel.username_taken(username):
			raise Exception('Duplicate username')

		user = UserEntity(username=username,
			google_id=google_id,
			email=email,
			password=password,
			admin=admin,
			parent = AppUserModel.user_key())

		return user.put()

	@staticmethod
	def get_user(id, serialize=False):

		user = UserEntity.query(UserEntity.google_id==id, 
			ancestor=AppUserModel.user_key()).get()

		if user is None:
			return False

		if serialize:
			return AppUserModel.serialize(user)

		return user



	@staticmethod
	def get_users(exclude=None, serialize=False):

		users = UserEntity.query(ancestor=AppUserModel.user_key()).fetch()

		logging.debug(exclude)

		if exclude is not None:
			exclude = long(exclude)
			key = AppUserModel.get_by_id(long(exclude)).key

			for user in users:
				if user.key == key:
					users.remove(user)

		if serialize:
			return [AppUserModel.serialize(user) for user in users]

		return user_json



	@staticmethod
	def get_by_username(username=None):

		try:

			if username is None:

				logging.debug('Username was none')
				raise Exception

			user = UserEntity.query(
				UserEntity.username==username,
				ancestor=AppUserModel.user_key()).get()

			if user is None:

				logging.debug('User entity with username ' + username + ' not found')
				raise Exception

			return user

		except Exception as e:

			raise Exception(e)


	@staticmethod
	def username_taken(username=None):

		try:

			# Check if username is None
			if username is None:

				raise Exception('Username was none')

			# Query user entities by username
			user = UserEntity.query(
				UserEntity.username==username,
				ancestor=AppUserModel.user_key()).get()

			# If user doesn't exist...
			if user is None:

				return False

			# If user does exists...
			return True

		# Catch exceptions
		except Exception as e:

			# Rethrow exceptions
			raise Exception(e)


	@staticmethod
	def get_other_users(id):

		users = UserEntity.query(UserEntity.key.id()!=id, 
			ancestor=AppUserModel.user_key())

		return users

	@staticmethod
	def get_by_id(id):
		try:
			return UserEntity.get_by_id(id=id, parent=AppUserModel.user_key())
		except Exception:
			return None

def serialize_time(t):
	t = time.mktime(t.utctimetuple()) * 1000
	t += getattr(t, 'microseconds', 0) / 1000
	return t