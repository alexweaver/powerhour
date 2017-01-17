app.factory('userService', ['$http', function($http) {
	return {

		getCurrentUser: function() {
			return $http.get('/api/v1/users/me').success(function(data) {
				return data;
			});
		},

		getOtherUsers: function(user_id) {
			var config = {
				'params': {
					'user_id': user_id
				}
			}

			return $http.get('/api/v1/users/other', config).success(function(data) {
				return data;
			});
		}
		
	};
}]);