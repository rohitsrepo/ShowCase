angular.module('module.tools')
.directive('fullscreen', ['analytics', function (analytics) {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			if(element.hasClass('disable')){
				return;
			}
			
			scope.isFullScreen = false;
			scope.isFullScreenDisable = false;

			var fullscreenCallback = function (status) {
				scope.$apply(function () {
					scope.isFullScreen = status;
				});
			};

			var painting;
			element.bind('click', function () {
				analytics.logEvent('Composition', 'ToolBar - Fullscreen: ' + scope.isFullScreen);
				painting = $('.painting').not('.ng-hide');
				painting.fullScreen({background: '#fff', callback: fullscreenCallback});
			});
		}
	};
}]);