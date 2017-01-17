app.directive('validateMixTitle', function () {
    'use strict';

    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attrs, ctrl) {
            ctrl.$validators.minLength = function (value) {
                if (value === undefined || value.length < 5) {
                    return false;
                }
                return true;
            };
            ctrl.$validators.maxLength = function (value) {
                if (value === undefined || value.length > 20) {
                    return false;
                }
                return true;
            };
        }
    };
});