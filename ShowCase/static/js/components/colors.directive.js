angular.module('module.color', [])
.directive('colorPalette', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			scope.isColorPaletteDisable = false;

			element.bind('click', function () {
				if(element.hasClass('disable')){
					return;
				}
			
				scope.$apply(function () {
					if (scope.isColorPaletteActive === undefined){
						var sourceImage = new Image();
						sourceImage.src = attrs["colorPalette"];
						var colorThief = new ColorThief();
						scope.dominantColor = colorThief.getColor(sourceImage);
						scope.palette = colorThief.getPalette(sourceImage, 7);
						scope.isColorPaletteActive = true;
					} else {
						scope.isColorPaletteActive = !scope.isColorPaletteActive;
					}
				});
			});
		}
	};
});