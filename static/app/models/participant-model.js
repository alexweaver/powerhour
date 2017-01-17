app.factory('ParticipantModel', ['UserModel', function (UserModel) {
    'use strict';

    var ParticipantModel = function (name, id) {
        UserModel.call(this, name, 'Particpants');
        var id = id;
        var userType = 

        this.getId = function() {return id;};
        this.setId = function(i) {id = i;};

        this.serialize = function () {
            return {
                'id': id
            }
        }
    };

    ParticipantModel.prototype = Object.create(UserModel.prototype);

    Object.defineProperty(ParticipantModel.prototype, 'id', {
        get: function () {return this.getId();},
        set: function (value) {this.setId(value);}
    });

    return ParticipantModel;
}]);