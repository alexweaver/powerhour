
def err(type, msg):
	raise eval(type + 'Error(\'' + msg + '\')')

class DuplicateError(ValueError):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)