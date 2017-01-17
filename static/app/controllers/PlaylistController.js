app.controller('PlaylistController', ['$scope', 'Playlist', '$routeParams', 'ClipModel', 'PlaylistModel', 'GuestModel', 'ParticipantModel', 'ClipService', 'ResponseConstants',
    function ($scope, Playlist, $routeParams, ClipModel, PlaylistModel, GuestModel, ParticipantModel, ClipService, ResponseConstants) {
    'use strict'; $scope.render = true;

    // Get route parameters
    var playlistId = $routeParams.playlistId;

    // Instantiate empty playlist with given id
    $scope.playlist = new PlaylistModel(playlistId);

    // Get playlist and instantiate data layer
    Playlist.get({id: playlistId, fields: []}, function(data) {

        var clips = data.clips;
        angular.forEach(clips, function(clip, i) {

            var id = clip.vid;
            var start = clip.start_seconds;
            var end = clip.end_seconds;

            var owner = undefined;
            if (ResponseConstants.PARTICIPANT in clip) {
                owner = new ParticipantModel(clip.participant.username, clip.participant.id);
            } else if (ResponseConstants.GUEST in clip) {
                owner = new GuestModel(clip.guest.username);
            }

            var duration = ClipService.parseTime(duration);
            var title = clip.title;

            clips[i] = new ClipModel(id, start, end, owner, duration, title);
        });

        var id = data.id;

        var author = data.author;
        author = new ParticipantModel(author.username, author.id);

        var title = data.title;

        var participants = data.participants;
        angular.forEach(participants, function(participant, i) {
            participants[i] = new ParticipantModel(participant.username, participant.id);
        });

        var guests = data.guests;
        angular.forEach(guests, function(guest, i) {
            guests[i] = new GuestModel(guest);
        });

        $scope.playlist = new PlaylistModel(id, author, title, participants, guests, clips);
        $scope.owner = $scope.playlist.getParticipant(0);
    });
}]);

app.constant('ResponseConstants', {
    'PARTICIPANT': 'participant',
    'GUEST': 'guest'
});