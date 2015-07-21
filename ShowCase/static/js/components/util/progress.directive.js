angular.module('module.util')
.directive('progressSupport', [ 'alert', function (alert) {
    return {
        restrict: 'E',
        replace: true,
        scope: {},
        template: '<div class="progress-bar"></div>',
    };
}]);