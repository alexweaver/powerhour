app.controller('MainController',[
	'$scope', 
	'$http',  
	'$location', 
	'$cookies', 
	function(
		$scope, 
		$http, 
		$location, 
		$cookies) {

	var user_param = 'current';

	$cookies.put('Bob', 'burgers');

}]);


app.controller('WelcomeController',['$scope', '$http', '$location', 'Auth', function($scope, $http, $location, Auth) {
	$scope.render = true;
		$scope.user = {};
		$scope.user.username = Auth.getUsername();
	}]);





app.controller('LoginController', [
	'$scope', 
	'$location',
	'Auth',
	function(
		$scope,
		$location,
		Auth) {





	$scope.login = function(username, password) {
		
		Auth.login(username, password).success(function(data) {

			$location.path('/welcome');

		});

	};





}]);





app.controller('CreateController', function(){});