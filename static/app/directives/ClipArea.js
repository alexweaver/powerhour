app.directive('clipArea', function (linkService) {
    'use strict';

    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attrs, ctrl) {
            ctrl.$parsers.push(function (value) {
                value = linkService.parse(value);
                return value;
            });
            ctrl.$validators.links = function (value) {
                if (value === undefined || value === false) {
                    return false;
                } return true;
            };
        }
    };
});