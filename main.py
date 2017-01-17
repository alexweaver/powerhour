#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from app.controllers.home_controller import *
from app.controllers.users import *
from app.controllers.playlists import *

import webapp2

app = webapp2.WSGIApplication([





	# webapp2.Route('/', MainHandler),
	# webapp2.Route('/welcome', MainHandler),
	# webapp2.Route('/playlist<:(/[a-zA-Z0-9]{11,})?>', MainHandler),
	# webapp2.Route('/profile', MainHandler),
	# webapp2.Route('/watch', MainHandler),
	# webapp2.Route('/register', MainHandler),
	# webapp2.Route('/logout', MainHandler),
	# webapp2.Route('/login', MainHandler),
	# webapp2.Route('/create', MainHandler),
	




	# User API calls

	webapp2.Route('/api/v1/users', UsersHandler),
	webapp2.Route('/api/v1/users/me', CurrentUserHandler),
	webapp2.Route('/api/v1/users/login', LoginHandler),
	webapp2.Route('/api/v1/users/logout', LogoutHandler),
	webapp2.Route('/api/v1/users/other', GetOtherUsers),
	webapp2.Route('/api/v1/register', RegisterHandler),
	webapp2.Route('/api/v1/login', LoginHandler),





	# Playlist API calls

	webapp2.Route('/api/v1/playlists/<playlist_id>/title<:/?>', PlaylistsTitleHandler),
	webapp2.Route('/api/v1/playlists/<playlist_id>/participants<:/?>', PlaylistsParticipantsHandler),
	webapp2.Route('/api/v1/playlists/<playlist_id>/guests', PlaylistsGuestsHandler),
	webapp2.Route('/api/v1/playlists/<playlist_id>/clips<:/?>', PlaylistsClipsHandler),
	webapp2.Route('/api/v1/playlists/<playlist_id>', PlaylistsHandler),
	webapp2.Route('/api/v1/playlists<:/?>', PlaylistsHandler),


	webapp2.Route('/<:.*>', MainHandler)




], debug=True)
