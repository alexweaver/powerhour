app.service('ClipService', function ($q, Video) {
    'use strict';


    this.parseTime = function (time) {

        if (typeof time !== 'string') {
            return 0;
        }

        var years = 0;
        var months = 0;
        var weeks = 0;
        var days = 0;

        var input = new RegExp('P[0-9YMWD]+T').exec(time);

        if (input !== null) {
            input = input[0];

            var years = new RegExp('[0-9]+Y').exec(input);
            years = years !== null ? parseInt(years[0].substring(0, years[0].length - 1)) : 0;
            years = years > 0 ? years * 365 * 24 * 60 * 60 : 0;
        
            var months = new RegExp('[0-9]+M').exec(input);
            months = months !== null ? parseInt(months[0].substring(0, months[0].length - 1)) : 0;
            months = months > 0 ? months * 30 * 24 * 60 * 60 : 0;

            var weeks = new RegExp('[0-9]+W').exec(input);
            weeks = weeks !== null ? parseInt(weeks[0].substring(0, weeks[0].length - 1)) : 0;
            weeks = weeks > 0 ? weeks * 7 * 24 * 60 * 60 : 0;

            var days = new RegExp('[0-9]+D').exec(input);
            days = days !== null ? parseInt(days[0].substring(0, days[0].length - 1)) : 0;
            days = days > 0 ? days * 24 * 60 * 60 : 0;

        }

        var hours = 0;
        var minutes = 0;
        var seconds = 0;

        var input = new RegExp('T[0-9HMS]+').exec(time);

        if (input !== null) {
            input = input[0];

            var hours = new RegExp('[0-9]+H').exec(input);
            hours = hours !== null ? parseInt(hours[0].substring(0, hours[0].length - 1)) : 0;
            hours = hours > 0 ? hours * 60 * 60 : 0;

            var minutes = new RegExp('[0-9]+M').exec(input);
            minutes = minutes !== null ? parseInt(minutes[0].substring(0, minutes[0].length - 1)) : 0;
            minutes = minutes > 0 ? minutes * 60 : 0;

            var seconds = new RegExp('[0-9]+S').exec(input);
            seconds = seconds !== null ? parseInt(seconds[0].substring(0, seconds[0].length - 1)) : 0;
        }

        return years + months + weeks + days + hours + minutes + seconds;
    }

var that = this;
    this.getDetails = function (vids) {

        if (vids.constructor !== Array) {
            throw "Video Ids not array";
        }

        var promises = [];
        console.log(vids);
        for (var i = 0; i < vids.length; i++) {

            var promise = Video.get({'id': vids[i]}).$promise;
            promises.push(promise);

        };

        var composite = $q.all(promises);

        return composite.then(function (data) {

            for (var i = 0; i < data.length; i++) {

                var item = data[i].items[0];

                data[i] = {

                    'id': item.id,
                    'duration': that.parseTime(item.contentDetails.duration),
                    'title': item.snippet.title

                };
                console.log(item);

            }

            return data;
        });

    }

});