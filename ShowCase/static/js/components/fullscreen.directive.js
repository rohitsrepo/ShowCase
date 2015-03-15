angular.module('module.fullscreen', [])
.directive('fullscreen', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			scope.isFullScreen = false;

			var fullscreenCallback = function (status) {
				scope.$apply(function () {
					scope.isFullScreen = status;
				});
			};

			var painting;
			element.bind('click', function () {
				painting = $('.painting').not('.ng-hide');
				painting.fullScreen({background: '#fff', callback: fullscreenCallback});
			});
		}
	};
});