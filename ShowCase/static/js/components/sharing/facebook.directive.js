angular.module('module.sharing')
.directive('facebookShare', ['$window', '$location', function ($window, $location) {
	'use strict';

	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var shareImage = $location.protocol() + '://' + $location.host() + attrs['source'];
			var shareUrl = $location.absUrl();
			var shareTitle = attrs['title'];
			var url = "https://www.facebook.com/dialog/share?app_id=462422103909005&display=popup&href=" +
			encodeURIComponent(shareUrl) + 
			"&redirect_uri=" + encodeURIComponent(shareUrl)
			element.bind('click', function () {
				$window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600')
			});
		}
	};
}]);



