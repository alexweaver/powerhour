app.directive('clipForm', function ($parse, Playlist, ClipService, ClipModel) {
    'use strict';

    return {
        restrict: 'A',
        require: 'form',
        scope: {playlist: '=', owner: '='},
        link: function (scope, elem, attrs, ctrl) {
            elem.bind('submit', function () {
                if (ctrl.$valid === false) {
                    alert('links invalid');
                    return;
                }
                console.log(scope.owner);
                var links = ctrl.links.$modelValue;

                var vids = [];
                var starts = [];
                for (var i = 0; i < links.length; i++) {
                    vids.push(links[i][0]);
                    starts.push(links[i][1]);
                }

                var promise = ClipService.getDetails(vids);
                promise.then(function (data) {
                    angular.forEach(data, function(value, key) {
                        var clip = new ClipModel(vids[key], starts[key], parseInt(starts[key]) + 60, scope.owner, value.duration, value.title);
                        if (starts[key] === undefined) {
                            clip.setMiddleInterval(60);
                        }
                        scope.playlist.addClip(clip);
                        console.log(scope.owner);
                    });
                    scope.playlist.saveClips();
                }); 
            });
        }
    };
});