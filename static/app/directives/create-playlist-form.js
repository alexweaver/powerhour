app.directive('createPlaylistForm', ['Playlist', 'Auth', '$location', function(PlaylistResource, Auth, $location) {
	return {
		restrict: 'A',
		require: 'form',
		link: function (scope, elem, attrs, ctrl) {
			elem.bind('submit', function () {
				if (ctrl.$valid === false) {
					alert('Invalid Title');
					return;
				}
				var data = {title: ctrl.playlistTitle.$modelValue, author: Auth.getUserId()};
				PlaylistResource.createPlaylist(data, function(data) {
					$location.path('/playlist/' + data['id']);
				});
			});
		}
	};
}]);