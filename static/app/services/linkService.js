app.service('linkService', function() {
    'use strict';

    function extractID(url) {
        var needle = 'watch?v=';
        var idLength = 11;

        var needleStart = url.indexOf(needle);
        if (needleStart !== -1) {
            var idStart = needleStart + needle.length;
            return url.substring(idStart, idStart + idLength);
        } else {
            return false;
        }
    }

    this.parse = function (links) {
        var links = links.split('\n');
        for (var i = 0; i < links.length; i++) {
            links[i] = links[i].match(/[^ ]+/g)
            var vid = extractID(links[i][0])
            var start = undefined;
            if (links[i].length > 1) {
                start = links[i][1];
            }
            links[i][1] = start;
            if (vid === false || links[i].length > 2) {
                return false;
            }
            links[i][0] = vid;
        }
        return links;
    };
});