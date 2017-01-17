app.factory('Playlist', ['$resource', 'ClipModel', function($resource, ClipModel) {
	
	return $resource('/api/v1/playlists/:id', {id: this.id}, {

		'update': {

			method: 'POST',

			transformRequest: function(inData) {

				var data = $.extend(true, {}, inData);

				for (var i = 0; i < data.participants.length; i++) {
					data.participants[i] = data.participants[i]['id'];
				}

				data.author = data.author['id'];

				for (var i = 0; i < data.clips.length; i++) {
					if (data.clips[i].owned) {
						data.clips[i].owner = data.clips[i].owner['id'];
					}
				}

				console.log(data);

				return angular.toJson(data);

			},

		},





		'addGuest': {
			url: '/api/v1/playlists/:id/guests',
			method: 'POST',
			isArray: true
		},

		'addParticipant': {
			url: '/api/v1/playlists/:id/participants',
			method: 'POST'
		},

		'deleteParticipant': {
			url: '/api/v1/playlists/:id/participants',
			method: 'DELETE'
		},

		'deleteGuest': {
			url: '/api/v1/playlists/:id/guests',
			method: 'DELETE'
		},

		'addClip': {
			url: '/api/v1/playlists/:id/clips',
			method: 'POST'
		},

		'saveClips': {
			url: '/api/v1/playlists/:id/clips',
			method: 'POST',
			transformRequest: function (data) {
				var data = $.extend(true, {}, data);
				console.log(data);
				angular.forEach(data['clips'], function(value, key) {
					data['clips'][key] = value.serialize();
				});
				return angular.toJson(data);
			}
		},





		'createPlaylist': {
			url: '/api/v1/playlists',
			method: 'POST'
		},





		'setTitle': {

			url: '/api/v1/playlists/:id/title',

			method: 'PUT'

		}

	});

}]);