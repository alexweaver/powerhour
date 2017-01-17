




app.controller('PlayerController', [
	'$scope', 
	'$http', 
	'$location', 
	'Playlist', 
	function(
		$scope, 
		$http, 
		$location, 
		Playlist) {





	$scope.shuffle = true;
	$scope.render = false;





	// Get all playlists for dropdown
	Playlist.query({}, function(data) {
		$scope.playlists = data;
		$scope.selectedPlaylist = data[0];
		$scope.render = true;
	});



	$scope.$watch('mix', function(newValue) {
		console.log(newValue)
	})

	$scope.play = function () {
		$scope.mix = $scope.selectedPlaylist.id;
		console.log($scope.mix);
	}

}]);