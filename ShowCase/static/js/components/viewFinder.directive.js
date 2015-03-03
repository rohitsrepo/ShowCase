angular.module('module.viewFinder', [])
.directive('viewFinder', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var isActive = false;
			var painting = $('.painting');
			element.bind('click', function () {
				if (!isActive){
					painting.zoome({hoverEf:'grayscale',showZoomState:true});
				} else {
					if(painting.parent().hasClass('zm-wrap'))
					{
						painting.unwrap().next().remove();
					}
				};
				isActive = !isActive;
			});
		}
	};
});