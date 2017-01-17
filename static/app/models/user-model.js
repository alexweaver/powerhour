app.factory('UserModel', [function () {
    'use strict';

    var UserModel = function (n, r) {

        var username = typeof n !== undefined
        ? n
        : '';

        var role = typeof r !== undefined
        ? r
        : 'User';
 
        this.getUsername = function () {return username;};
        this.setUsername = function (n) {username = n;};

        this.getRole = function () {return role;};
        this.setRole = function (r) {role = r;};

        this.serialize = function () {return {username: username};};
    };

    Object.defineProperty(UserModel.prototype, 'username', {
        get: function () {return this.getUsername();},
        set: function (value) {this.setUsername(value);}
    });

    Object.defineProperty(UserModel.prototype, 'role', {
        get: function () {return this.getRole();},
        set: function (value) {this.setRole(value);}
    })

    return UserModel;
}]);