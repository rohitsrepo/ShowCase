angular.module('module.panZoom', [])
.directive('panZoom', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var isActive = false;
			var painting = $('.painting');
			
			element.bind('click', function () {
				if (!isActive){
					painting.panzoom({
						$zoomIn: $(".zoom-in"),
			            $zoomOut: $(".zoom-out"),
			            $reset: $(".reset")
					});
				} else {
					painting.panzoom('reset');
					painting.panzoom('destroy');
				}

				isActive = !isActive;
			});
		}
	};
});