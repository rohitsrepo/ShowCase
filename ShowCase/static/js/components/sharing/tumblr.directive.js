angular.module('module.sharing')
.directive('tumblrShare', ['$window', '$location', function ($window, $location) {
	'use strict';

	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var shareImage = $location.protocol() + '://' + $location.host() + attrs['source'];
			var shareUrl = $location.absUrl();
			var url = "http://www.tumblr.com/share/photo?source="+
			encodeURIComponent(shareImage)+"&caption="+(attrs['description'])+"&clickthru="+encodeURIComponent(shareUrl);
			element.bind('click', function () {
				$window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600')
			});
		}
	};
}]);



