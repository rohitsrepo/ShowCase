angular.module('module.sharing')
.directive('pinterestShare', ['$window', '$location', 'analytics', function ($window, $location, analytics) {
	'use strict';

	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var baseUrl = $location.protocol() + '://' + $location.host() + ':' + $location.port();
			var shareImage = baseUrl + attrs['source'];
			var shareUrl = baseUrl + attrs['shareUrl'] + '#?scrollTo=painting';
			var url = "http://pinterest.com/pin/create/bookmarklet/?media="+encodeURIComponent(shareImage)+
			"&url="+encodeURIComponent(shareUrl)+"& is_video=false&description="+encodeURIComponent(attrs['description']);
			element.bind('click', function () {
				if(baseUrl.indexOf("arts") > -1){
					analytics.logEvent("Composition", "Social-Share: Pinterest");
				} else {
					analytics.logEvent("Reader", "Social-Share: Pinterest");
				}
				
				$window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600')
			});
		}
	};
}]);



