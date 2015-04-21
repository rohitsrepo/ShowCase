angular.module('module.tools')
.directive('viewFinder', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			scope.isViewFinderActive = false;
			scope.isViewFinderDisable = false;

			var painting;
			element.bind('click', function () {
				analytics.logEvent('Composition', 'click', 'ToolBar - ViewFinder: ' + scope.isViewFinderActive);

				if(element.hasClass('disable')){
					return;
				}
				
				if (!scope.isViewFinderActive){
					painting = $('.painting').not(".ng-hide");
					painting.zoome({hoverEf:'grayscale',showZoomState:true,magnifierSize:[200,200]});
				} else {
					if(painting.parent().hasClass('zm-wrap'))
					{
						painting.unwrap().next().remove();
					}
				}
				scope.$apply(function () {
					scope.isViewFinderActive = !scope.isViewFinderActive;
					if (scope.isViewFinderActive) {
						scope.isFullScreenDisable = true;
						scope.isPanZoomDisable = true;
						scope.isGrayScaleDisable = true;
						scope.isOutlineDisable = true;
					} else {
						scope.isFullScreenDisable = false;
						scope.isPanZoomDisable = false;
						scope.isGrayScaleDisable = false;
						scope.isOutlineDisable = false;
					}
				});
			});
		}
	};
});