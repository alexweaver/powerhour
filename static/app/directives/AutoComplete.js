app.directive('autoComplete', ['$parse', 'userService', 'Auth', 'Playlist', 'PlaylistModel', 'GuestModel', 'ParticipantModel',
	function($parse, userService, Auth, Playlist, PlaylistModel, GuestModel, ParticipantModel) {
	
	return {

		scope: {playlist: '='},
		link: function(scope, elem, attr, ctrl) {

			userService.getOtherUsers(Auth.getUserId()).success(function(data) {
				for (var i = 0; i < data.length; i++) {
					data[i].label = data[i].username;
				}

				elem.autocomplete({
					source: data,
					focus: function(event, ui) {
        				elem.val(ui.item.username);
        				return false;
      				},
      				select: function(event, ui) {

      					event.stopImmediatePropagation();
      					elem.val('');

      					var participant = new ParticipantModel(ui.item.username, ui.item.id);
      					scope.playlist.addParticipant(participant);
 

      					return false;
      				}
				});

				elem.bind('keydown', function (event) {
					if (event.which === 13) {
						var guest = new GuestModel(elem.val());
						scope.playlist.addGuest(guest);
						scope.playlist.saveGuest(guest);
						scope.$apply();

						elem.autocomplete('close');
						elem.val('');
					}
				});

			});
		}
	};
}]);