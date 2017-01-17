from entities import UniqueIDEntity

from google.appengine.ext import ndb

class UniqueIDModel():

	def unique_id_key():
		return ndb.Key('Unqiue ID', 'Default Unique ID Key')

	@staticmethod
	def get_id(model_type=None):
		unique_id = UniqueIDEntity.query(model_type=model_type, 
			ancestor=unique_id_key()).get()

		if unique_id is None:
			unique_id = UniqueIDEntity(model_type=model_type, id=0, 
				parent=unique_id_key())

		id = unique_id.id
		unique_id.id = unique_id.id + 1

		unique_id.put()

		return id