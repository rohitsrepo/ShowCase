angular.module('module.sharing')
.directive('pinterestShare', ['$window', '$location', function ($window, $location) {
	'use strict';

	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var shareImage = $location.protocol() + '://' + $location.host() + attrs['source'];
			var shareUrl = $location.absUrl();
			var url = "http://pinterest.com/pin/create/bookmarklet/?media="+encodeURIComponent(shareImage)+
			"&url="+encodeURIComponent(shareUrl)+"& is_video=false&description="+encodeURIComponent(attrs['description']);
			element.bind('click', function () {
				$window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600')
			});
		}
	};
}]);



