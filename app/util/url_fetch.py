from google.appengine.api import urlfetch
from google.appengine.api import memcache

import json
import logging

def get_request(url):
	result = urlfetch.fetch(url=url, method=urlfetch.GET)
	return json.loads(result.content)

def search_youtube_id(id, part):

	url = 'https://www.googleapis.com/youtube/v3/videos/?'
	url += 'id=' + id
	url += '&part=' + part
	url += '&key=AIzaSyAHWaWndU1hwDhQCnmQ7PcxX4bzoozWHwk'

	return get_request(url)

def get_snippet(id=None):

	snippet = memcache.get(id + '-snippet')

	if snippet is None:
		logging.debug(id)
		snippet = search_youtube_id(id, 'snippet')
		logging.debug(snippet)
		snippet = snippet['items'][0]['snippet']
		memcache.add(id + '-snippet', snippet)

	return snippet

def get_details(id=None):

	details = memcache.get(id + '-details')

	if details is None:
		details = search_youtube_id(id, 'contentDetails')
		details = details['items'][0]['contentDetails']
		memcache.add(id + '-details', details)

	return details