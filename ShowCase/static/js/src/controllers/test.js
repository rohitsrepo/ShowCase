var testCtrlModule = angular.module('controller.test', ['angularFileUpload']);

testCtrlModule.controller('testCtrl', ['$scope', '$upload', function ($scope, $upload) {
    console.log('Test controller initialized');
}]);

testCtrlModule.directive('elevatez', function () {
    return {
        restrict: 'A',
        scope: {
            option: "="
        },
        link: function (scope, element, attrs) {
            console.log('calling the elevateZoom', scope.option);
            element.elevateZoom(scope.option);
        }
    }
});