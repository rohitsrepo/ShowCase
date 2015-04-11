angular.module('module.sharing')
.directive('facebookShare', ['$window', '$location', function ($window, $location) {
	'use strict';

	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var baseUrl = $location.protocol() + '://' + $location.host() + ':' + $location.port();
			var shareUrl = baseUrl + attrs['shareUrl'] + '#?scrollTo=painting&closeTab=yes';
			var url = "https://www.facebook.com/dialog/share?app_id=462422103909005&display=popup&href=" +
			encodeURIComponent(shareUrl) + 
			"&redirect_uri=" + encodeURIComponent('http://thirddime.com/')
			element.bind('click', function () {
				$window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600')
			});
		}
	};
}]);



