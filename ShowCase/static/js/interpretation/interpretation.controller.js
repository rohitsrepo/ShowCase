angular.module("InterpretationApp")
.controller('interpretationController', ['$scope', function($scope) {
    $scope.hideName = true;
    $scope.interpretation = {};

    $scope.init = function (is_admired, is_bookmarked) {
        $scope.interpretation.is_admired = is_admired == 'True';
        $scope.interpretation.is_bookmarked = is_bookmarked == 'True';
    };

    $scope.handleAdmire = function () {
        $scope.interpretation.is_admired = !$scope.interpretation.is_admired;
    }

    $scope.handleBookmark = function () {
        $scope.interpretation.is_bookmarked = !$scope.interpretation.is_bookmarked;
    }
    

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