app.directive('videoClip', function($parse) {
	return {
		restrict: 'A',
		templateUrl: '/static/app/views/home.html',
		link: function (scope, elem, attrs) {
			var index = attrs.index + 1;


			// scope.$watch(attrs.videoClip, function(newValue, oldValue) {
				
			// 	newValue.url = 'www.youtube.com/watch?v=' + newValue.vid

			// 	if (newValue.start_seconds !== oldValue.start_seconds) {
			// 		youtubeService.getVideoDetails(newValue.vid).success(function(data) {
			// 				var clip = newValue;
			// 				clip.end_seconds = Math.min(newValue.start_seconds + 60, convertISO8601ToSeconds(data['items'][0]['contentDetails']['duration']));
			// 				$parse(attrs.videoClip).assign(scope, clip);	
			// 		});
			// 	}

			// 	else if (newValue.end_seconds !== oldValue.end_seconds) {
			// 		var clip = newValue;
			// 		clip.start_seconds = Math.max(clip.end_seconds - 60, 0);
			// 		$parse(attrs.videoClip).assign(scope, clip);	
			// 	}

			// }, true);

			$(elem).hover(
				function() { elem.find('.delete-container').css('display', 'inline'); },
				function() { elem.find('.delete-container').css('display', 'none'); }
			);
		}
	};	
})
