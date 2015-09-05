angular.module('module.tools')
.directive('panZoom', ['analytics', function (analytics) {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			scope.isPanZoomActive = false;
			scope.isPanZoomDisable = false;

			var painting = $('.painting');

			element.bind('click', function () {
				analytics.logEvent('Composition', 'ToolBar - PanZoom: ' + scope.isPanZoomActive);
				if(element.hasClass('disable')){
					return;
				}

				if (!scope.isPanZoomActive){
					painting.panzoom({
						$zoomIn: $(".zoom-in"),
			            $zoomOut: $(".zoom-out"),
			            $reset: $(".zoom-reset")
					});
				} else {
					painting.panzoom('reset');
					painting.panzoom('destroy');
				}

				scope.$apply(function () {
					scope.isPanZoomActive = !scope.isPanZoomActive;
				});
			});
		}
	};
}]);