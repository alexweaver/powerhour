from google.appengine.ext import ndb;

from entities.permission_entity import PermissionEntity

import logging


class PermissionModel():
	
	@staticmethod
	def permission_key():
		return ndb.Key('Clip', 'Default Permission Key')

	@staticmethod
	def create_permission(user=None, subject=None, admin=False, edit=False, 
		view=False):
		debug('Creating permission')

		permission = PermissionEntity(user=user, subject=subject, admin=admin, 
			edit=edit, view=view, parent=PermissionModel.permission_key())

		return permission.put()

	@staticmethod
	def get_permission(user=None, subject=None):
		debug('Getting permission')

		permission = PermissionEntity.query(PermissionEntity.user==user,
			PermissionEntity.subject==subject, 
			ancestor=PermissionModel.permission_key())

		return permission

	@staticmethod
	def get_editors(subject=None):
		debug('Getting editors')

		permissions = PermissionEntity.query(PermissionEntity.subject==subject,
			PermissionEntity.edit==True, 
			ancestor=PermissionModel.permission_key())

		editors = [permission.user for permission in permissions]

		return editors

TAG = 'PermissionModel'

def debug(msg):
	logging.debug(TAG + ' - ' + msg)