app.directive('player', function($window, Playlist) {
	return {
		restrict: 'E',
		link: function(scope, elem, attrs) {





			var clips = [];
			var vindex;
			var player;
			var previousState = -1;





			if (typeof YT === 'undefined') {

				$window.onYouTubeIframeAPIReady = function() {

					init();

				}

			} else if (typeof player === 'undefined') {

				init();

			}





			scope.$watch(attrs.mix, function(newValue) {
				console.log(newValue);
				if (typeof newValue !== 'undefined') {

					var params = {
						'id': newValue,
						'shuffle': true
					}

					Playlist.get(params, function(data) {
						console.log(data);
						clips = data.clips;
						vindex = 0;
						loadVideoByIndex(0);
					});

				}

			});



			function onPlayerStateChange(event) {
			    if (vindex < clips.length - 1) {
			        if (player.getPlayerState() === YT.PlayerState.ENDED && previousState !== YT.PlayerState.UNSTARTED) {
			            vindex++;
			            loadVideoByIndex(vindex);
			        }
			    }
			    previousState = player.getPlayerState();
			}





			function loadVideoByIndex(i) {

			    var clip = clips[i];
			    var videoToPlay = {
			        'videoId': clip.vid,
			        'startSeconds': clip.start_seconds,
			        'endSeconds': clip.end_seconds
			    }
			    player.loadVideoById(videoToPlay);
			}





			function init() {

				YT.PlayerState.UNSTARTED = -1;
				player = new YT.Player('player', {
					playerVars: {
						controls: 0
					},
					height: '390',
					width: '640',
					events: {
						'onStateChange': onPlayerStateChange
					}
				});

			}

			elem.keypress(function(e) {
				if (e.which === 78) {
					loadVideoByIndex(vindex++);
				}
			});
			

		}

	};

});