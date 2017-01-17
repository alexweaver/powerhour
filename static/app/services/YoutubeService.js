app.factory('Video', function($resource) {

	return $resource('https://www.googleapis.com/youtube/v3/videos',

		{

			'key': 	'AIzaSyAHWaWndU1hwDhQCnmQ7PcxX4bzoozWHwk',
			'part': 'snippet,contentDetails'

		},

		{

			'get': {

				transformResponse: function(data) {

					return angular.fromJson(data);
					
				}

			}

		}

	)

});