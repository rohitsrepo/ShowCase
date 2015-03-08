angular.module('module.panZoom', [])
.directive('panZoom', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			scope.isPanZoomActive = false;
			var painting = $('.painting');
			
			element.bind('click', function () {
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
				});
			});
		}
	};
});