angular.module('module.color', [])
.directive('colorPalette', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			element.bind('click', function () {
				scope.$apply(function () {
					if (scope.showPalette === undefined){
						var sourceImage = new Image();
						sourceImage.src = attrs["colorPalette"];
						var colorThief = new ColorThief();
						scope.dominantColor = colorThief.getColor(sourceImage);
						scope.palette = colorThief.getPalette(sourceImage, 7);
						scope.showPalette = true;
					} else {
						scope.showPalette = !scope.showPalette;
					};
				});
			});
		}
	};
});