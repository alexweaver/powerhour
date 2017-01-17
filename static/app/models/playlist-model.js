app.factory('PlaylistModel', ['Playlist', 'ParticipantModel', 'GuestModel',
	function (PlaylistResource, ParticipantModel, GuestModel) {
    'use strict';

    var PlaylistModel = function (i, a, t, p, g, c) {

        var id = typeof i !== 'undefined' ? i : '';
        var author = typeof a !== 'undefined' ? a : {};
        var title = typeof t !== 'undefined' ? t : '';
        var participants = typeof p !== 'undefined' ? p : [];
        var guests = typeof g !== 'undefined' ? g : [];
        var clips = typeof c !== 'undefined' ? c : [];
        var users = [];

        /* GETTERS AND SETTERS */

        this.getId = function () {return id;};
        this.setId = function (i) {id = i;};

        this.getAuthor = function () {return author;};
        this.setAuthor = function (a) {author = a;};

        this.getTitle = function () {return title;};
        this.setTitle = function (t) {title = t;};

        this.getParticipants = function () {return participants;};
        this.getParticipant = function (index) {return participants[index];};

        this.getGuests = function () {return guests;};
        this.addGuest = function (g) {if (!this.hasGuest(g)) {guests.push(g); this.refreshUsers();}};
        this.removeGuest = function (g) {guests.splice(guests.indexOf(g), 1);};
        this.hasGuest = function (g) {return guests.indexOf(g) > -1;};

        this.getUsers = function () {return users;};
        this.setUsers = function (u) {users = u;};
        this.refreshUsers = function() {users = participants.concat(guests)};

        this.refreshUsers();

        this.getClips = function () {return clips;};
        this.setClips = function (c) {clips = c;};
        this.addClip = function (c) {clips.push(c);};

        this.saveTitle = function () {
            var templateData = {id: this.getId()};
            var payload = {title: this.getTitle()};
            PlaylistResource.setTitle(templateData, payload);
        };

        /* RESOURCE METHODS */

        this.saveGuest = function (guest) {
            var templateData = {id: id};
            var payload = {guest: guest.username}; // change
            PlaylistResource.addGuest(templateData, payload);
        };

        this.saveClips = function () {
            var templateData = {id: this.getId()};
            var payload = {clips: this.clips};
            PlaylistResource.saveClips(templateData, payload);
        };

        this.addParticipant = function (participant) {
            this.participants.push(participant);
            var templateData = {id: this.getId()};
            var payload = {participant: participant.id};
            PlaylistResource.addParticipant(templateData, payload);
            this.refreshUsers();
        };

        this.deleteUser = function (user) {
            if (user instanceof ParticipantModel) {
                participants.splice(participants.indexOf(user), 1);
                var data = {id: id, participant: user.id};
                PlaylistResource.deleteParticipant(data);
            } else if (user instanceof GuestModel) {
                guests.splice(guests.indexOf(user), 1);
                var data = {id: id, guest: user.username};
                PlaylistResource.deleteGuest(data);
            } else {
                return false;
            }
            this.refreshUsers();
            return true;
        };

        this.getTotalDuration = function () {
            var total = 0;
            angular.forEach(clips, function(clip) {
                total += clip.end - clip.start;
            });
            return total;
        }
    };

    /* DEFINE PROPERTIES */

    Object.defineProperty(PlaylistModel.prototype, 'pid', {
        get: function () {return this.getId();},
        set: function (value) {this.setId(value);}
    });

    Object.defineProperty(PlaylistModel.prototype, 'title', {
        get: function () {return this.getTitle();},
        set: function (value) {this.setTitle(value);}
    });

    Object.defineProperty(PlaylistModel.prototype, 'author', {
        get: function () {return this.getAuthor();},
        set: function (value) {this.setAuthor(value);}
    });

    Object.defineProperty(PlaylistModel.prototype, 'participants', {
        get: function () {return this.getParticipants();},
        set: function (value) {this.setParticipants(value);}
    });

    Object.defineProperty(PlaylistModel.prototype, 'guests', {
        get: function () {return this.getGuests();},
        set: function (value) {this.setGuests(value);}
    });

    Object.defineProperty(PlaylistModel.prototype, 'users', {
        get: function () {return this.getUsers();}
    });

    Object.defineProperty(PlaylistModel.prototype, 'clips', {
        get: function () {return this.getClips();},
        set: function (value) {this.setClips(value);}
    });

    Object.defineProperty(PlaylistModel.prototype, 'totalDuration', {
        get: function() {return this.getTotalDuration();}
    });

    Object.defineProperty(PlaylistModel.prototype, 'length', {
        get: function() {return this.clips.length;}
    });

    return PlaylistModel;
}]);