angular.module('PostApp')
.directive('interheight', ['$rootScope', '$timeout', function ($rootScope, $timeout) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            imagesLoaded(element, function () {
                $timeout(function () {
                    var parent = element.parent();
                    parent.css('height', element[0].offsetHeight);
                });
            });
        }
    };
}]);