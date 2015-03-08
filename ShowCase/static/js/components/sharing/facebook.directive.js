angular.module('module.sharing')
.directive('facebookShare', ['$window', '$location', function ($window, $location) {
	'use strict';

	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var shareImage = $location.protocol() + '://' + $location.host() + attrs['source'];
			var shareUrl = $location.absUrl();
			var shareTitle = attrs['title'];
			var url = "http://www.facebook.com/sharer.php?s=100&p[title]="+(shareUrl)+"&p[summary]="+
			attrs['description']+"&p[url]="+encodeURIComponent(shareUrl)+"&p[images][0]="+(shareImage)
			element.bind('click', function () {
				$window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600')
			});
		}
	};
}]);



