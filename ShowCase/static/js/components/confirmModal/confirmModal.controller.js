angular.module('module.confirmModal')
.controller('confirmModalController', ['$scope',
    'data',
    'close',
    'progress',
    'alert',
    function ($scope, data, close, progress, alert) {
        $scope.data = data;

        $scope.confirm = function () {
            close('confirm');
        }

        $scope.deny = function () {
            close('deny');
        }
    }
]);