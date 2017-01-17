app.directive('mainNav', function($location, $route, Auth) {
	return {
		restrict: 'A',
		templateUrl: '/static/app/views/nav.html',
		link: function(scope, elem, attrs, ctrl) {

			scope.loggedIn = Auth.isLoggedIn();

			scope.logout = function() {
				Auth.logout();
				$location.path('/');
				$route.reload();
			}

		}
	};
});