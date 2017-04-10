angular.module("InterpretationApp")
.controller('interpretationController', ['$scope', function($scope) {
	$scope.hideName = true;

	$scope.init = function () {

	};
	
    var siteHeader = document.querySelector('.site-header');
    siteHeader.className += " white";

}]).directive('fitImage', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            element.bind('load', function () {
               imgElement = element[0]
               var imgClass = (imgElement.width/imgElement.height > 1) ? 'landscape' : 'potrait';
               element.addClass(imgClass);
            })
        }
    }
});