app.directive('userDeleteButton', [function() {
	'use strict';

	return {
		restrict: 'A',
		scope: {playlist: '=', user: '='},
		link: function(scope, elem, attrs, ctrl) {
			elem.bind('click', function() {
				scope.playlist.deleteUser(scope.user);
				scope.$apply();
			});
		}
	};
}]);