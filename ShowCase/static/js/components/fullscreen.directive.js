angular.module('module.fullscreen', [])
.directive('fullscreen', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			scope.isFullScreen = false;

			var fullscreenCallback = function (status) {
				if (!status) {
					scope.isFullScreen = false;
				}
			};

			var painting = $('.painting');
			element.bind('click', function () {
				painting.fullScreen({background: '#fff', callback: fullscreenCallback});
				scope.isFullScreen = true;
			});
		}
	};
});