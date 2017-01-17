app.factory('ClipModel', ['ParticipantModel', 'GuestModel', 'Auth', function (ParticipantModel, GuestModel, Auth) {
    'use strict';

    var ClipModel = function (v, s, e, o, d, t) {

        var id = v !== undefined
            ? v
            : '';

        var duration = d !== undefined
            ? d
            : 0;

        var start = s !== undefined 
            ? Math.max(s, 0)
            : 0;

        var end = e !== undefined
            ? Math.max(s, e)
            : 0;

        var owner = o !== undefined
            ? o
            : {};

        var title = t !== undefined
            ? t
            : '';

        var creator = Auth.getUserId();

        this.getId = function () {return id;};
        this.setId = function (i) {id = i;};

        this.getStart = function () {return start;};
        this.setStart = function (s) {start = Math.max(s, 0);};

        this.getEnd = function () {return end;};
        this.setEnd = function (e) {end = Math.max(e, 0);};

        this.getDuration = function () {return duration;};
        this.setDuration = function (d) {duration = Math.max(d, 0);};

        this.getOwner = function () {return owner;};
        this.setOwner = function (o) {owner = o;};

        this.getTitle = function () {return title;};
        this.setTitle = function (t) {title = t;};

        this.setInterval = function (s, e) {
            s = Math.max(s, 0);
            e = Math.max(e, 0);
            e = Math.min(e, duration);
            this.setStart(s);
            this.setEnd(e);
        };

        this.setFullVideoInterval = function () {
            this.setStart(0);
            this.setEnd(duration);
        };

        this.setMiddleInterval = function (l) {
            if (l >= this.getDuration()) {
                this.setFullVideoInterval();
            } else {
                var s = parseInt((this.getDuration() - l) / 2);
                var e = Math.min(s + l, this.getDuration());
                this.setInterval(s, e);
            }            
        };

        this.serialize = function () {

            var data = {
                'vid': this.id,
                'start': this.start,
                'end': this.end,
                'creator': creator
            };

            if (owner instanceof ParticipantModel) {
                data.participant = owner.id;
            } else {
                data.guest = owner.username;
            }

            return data;
            
        };
    };

    var proto = ClipModel.prototype;

    Object.defineProperty(proto, 'id', {
        get: function () {return this.getId();}
    });

    Object.defineProperty(proto, 'start', {
        get: function() {return this.getStart();},
        set: function(value) {this.setStart(value);}
    });

    Object.defineProperty(proto, 'end', {
        get: function () {return this.getEnd();},
        set: function (value) {this.setEnd(value);}
    });

    Object.defineProperty(proto, 'title', {
        get: function() {return this.getTitle();},
        set: function(value) {this.setTitle(value);}
    });

    Object.defineProperty(proto, 'owner', {
        get: function () {return this.getOwner();},
        set: function (value) {this.setOwner(value);}
    });

    Object.defineProperty(proto, 'url', {
        get: function() {return 'www.youtube.com/watch?v=' + this.id;}
    });

    Object.defineProperty(proto, 'thumbnail', {
        get: function() {return 'http://img.youtube.com/vi/' + this.id + '/mqdefault.jpg';}
    });
 
    return ClipModel;
}]);