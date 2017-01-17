import webapp2

from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
	def get(self, route):
		self.response.write(template.render('app/templates/main.html', {}))