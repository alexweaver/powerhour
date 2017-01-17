




app.controller('RegisterController', [
	'$scope', 
	'$http', 
	'$location', 
	'Auth', 
	function(
		$scope, 
		$http, 
		$location, 
		Auth) {





	$scope.register = function() {
		console.log($scope.username, $scope.password);
		Auth.register($scope.username, $scope.password)

		.success(function(data) {
			$location.path('/welcome');
		});

	};





}]);