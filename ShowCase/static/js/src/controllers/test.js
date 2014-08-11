var testCtrlModule = angular.module('controller.test', ['angularFileUpload']);

testCtrlModule.controller('testCtrl', ['$scope', '$upload', function ($scope, $upload) {
    console.log('Test controller initialized');
    $scope.zoomeOptions = {hoverEf: 'grayscale', showZoomState: true, zoomRange: [1, 5], zoomStep: 0.5, defaultZoom: 1.5, magnifierSize: [200, 200], borderSize: 1000};
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

testCtrlModule.directive('shoot', function () {
    return {
        restrict: 'E',
        link: function (scope, element, attrs) {
            var config = {
                image : '/static/img/callout.jpg',
                blurLevel	: 6,
                opacity	: 0.8
                    };

            element.photoShoot(config);
        }
    }
});

testCtrlModule.directive('zoome', function () {
    return {
        restrict: 'A',
        scope: {
            zoomeOptions: '='
        },
        link : function (scope, element, attrs) {
            console.log("Zoome options: ", scope.zoomeOptions);
            console.log("Zoome element: ", element);
            element.zoome(scope.zoomeOptions);
            
            scope.$watch('zoomeOptions', function (newVal, oldVal) {
                if (newVal === oldVal){
                    return;
                }
                console.log('sensing a change in the zoomeOptions: ', newVal);
                if(element.parent().hasClass('zm-wrap')){
                    element.unwrap().next().remove();
                }
                
                element.zoome(newVal);
            }, true);
        }
    }
});