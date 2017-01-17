app.controller('ProfileController', [
	'$scope', 
	'$location', 
	'Playlist', 
	'userService', 
	function(
		$scope, 
		$location, 
		Playlist, 
		userService) {
	
	userService.getCurrentUser().success(function(data) {
		console.log(data);

		var params = { 'user': data['id'] }

		Playlist.query(params, function(data) {
			$scope.playlists = data;
			$scope.selectedPlaylist = data[0];
		});

	});

	$scope.edit = function() {
		$location.path('playlist').search({'m': $scope.selectedPlaylist['id']});
	}
	
}]);