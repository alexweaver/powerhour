app.directive('titleForm', function () {
    'use strict';

    return {
        restrict: 'A',
        require: 'form',
        scope: {playlist: '='},
        link: function (scope, elem, attrs, ctrl) {
            elem.bind('submit', function () {
                if (ctrl.$valid === false) {
                    alert('check title');
                    return;
                }
                scope.playlist.saveTitle();
            });
        }
    };
});