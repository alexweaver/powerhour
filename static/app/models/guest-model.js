app.factory('GuestModel', ['UserModel', function (UserModel) {
    'use strict';

    var GuestModel = function (name) {
        UserModel.call(this, name, 'Guests');

        this.encode = function (index) {
            return JSON.stringify(['guest', index]);
        };
    };

    GuestModel.prototype = Object.create(UserModel.prototype);

    return GuestModel;
}]);