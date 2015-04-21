angular.module('module.tools')
.directive('panZoom', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			scope.isPanZoomActive = false;
			scope.isPanZoomDisable = false;

			var painting = $('.painting');
			
			element.bind('click', function () {
				analytics.logEvent('Composition', 'click', 'ToolBar - PanZoom: ' + scope.isPanZoomActive);
				if(element.hasClass('disable')){
					return;
				}
			
				if (!scope.isPanZoomActive){
					painting.panzoom({
						$zoomIn: $(".zoom-in"),
			            $zoomOut: $(".zoom-out"),
			            $reset: $(".reset")
					});
				} else {
					painting.panzoom('reset');
					painting.panzoom('destroy');
				}

				scope.$apply(function () {
					scope.isPanZoomActive = !scope.isPanZoomActive;
					if (scope.isPanZoomActive) {
						scope.isFullScreenDisable = true;
						scope.isViewFinderDisable = true;
						scope.isGrayScaleDisable = true;
						scope.isOutlineDisable = true;
					} else {
						scope.isFullScreenDisable = false;
						scope.isViewFinderDisable = false;
						scope.isGrayScaleDisable = false;
						scope.isOutlineDisable = false;
					}
				});
			});
		}
	};
});