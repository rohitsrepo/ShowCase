angular.module('module.sharing')
.directive('tumblrShare', ['$window', '$location', 'analytics', function ($window, $location, analytics) {
	'use strict';

	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var baseUrl = $location.protocol() + '://' + $location.host() + ':' + $location.port();
			var shareImage = baseUrl + attrs['source'];
			var shareUrl = baseUrl + attrs['shareUrl'] + '#?scrollTo=painting';
			var url = "http://www.tumblr.com/share/photo?source="+
			encodeURIComponent(shareImage)+"&caption="+encodeURIComponent(attrs['description'])+"&clickthru="+encodeURIComponent(shareUrl);
			element.bind('click', function () {
				if(baseUrl.indexOf("arts") > -1){
					analytics.logEvent("Composition", "Social-Share: Tumblr");
				} else {
					analytics.logEvent("Reader", "Social-Share: Tumblr");
				}
				
				$window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600')
			});
		}
	};
}]);



