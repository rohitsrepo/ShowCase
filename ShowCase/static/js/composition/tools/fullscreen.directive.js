angular.module('module.tools')
.directive('fullscreen', function () {
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
				analytics.logEvent('Composition', 'click', 'ToolBar - Fullscreen: ' + scope.isFullScreen);
				painting = $('.painting').not('.ng-hide');
				painting.fullScreen({background: '#fff', callback: fullscreenCallback});
			});
		}
	};
});