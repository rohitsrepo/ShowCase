angular.module('module.viewFinder', [])
.directive('viewFinder', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			scope.isViewFinderActive = false;
			var painting = $('.painting');
			element.bind('click', function () {
				if (!scope.isViewFinderActive){
					painting.zoome({hoverEf:'grayscale',showZoomState:true,magnifierSize:[200,200]});
				} else {
					if(painting.parent().hasClass('zm-wrap'))
					{
						painting.unwrap().next().remove();
					}
				}
				scope.$apply(function () {
					scope.isViewFinderActive = !scope.isViewFinderActive;
				});
			});
		}
	};
});