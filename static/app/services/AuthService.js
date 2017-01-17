app.factory('Auth', ['$http', '$cookies', '$location', function($http, $cookies, $location) {

	return {





		register: function(username, password) {

			var payload = {

				'username': username,
				'password': password

			};
			
			var promise = $http.post('/api/v1/register', payload);

			promise.success(function(data) {

				$cookies.put('userid', data['id']);
				$cookies.put('username', data['username']);

			});

			promise.error(function(data) {

				alert(data);

			});

			return promise;

		},





		login: function(username, password) {

			var payload = {

				'username': username,
				'password': password

			};

			var promise = $http.post('/api/v1/login', payload);

			promise.success(function(data) {

				$cookies.put('userid', data['id']);
				$cookies.put('username', data['username']);

			});

			promise.error(function(data) {

				alert(data);

			});

			return promise;

		},





		logout: function() {

			$cookies.remove('username');
			$cookies.remove('userid');
			$location.path('/');

		},





		isLoggedIn: function() {

			return $cookies.get('userid') ? true : false;

		},





		getUsername:function () {

			return $cookies.get('username');

		},





		getUserId: function() {
			return parseInt($cookies.get('userid'));
		}





	};

}]);