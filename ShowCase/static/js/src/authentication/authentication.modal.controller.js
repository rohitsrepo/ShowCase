angular.module('authentication')
.controller('authenticationModalController', ['$scope', '$modalInstance', 'authenticationService', function ($scope, $modalInstance, authenticationService) {
    'use strict';
    
    $scope.authError = '';
    
    $scope.login = function (user) {
        $scope.authError = '';
        authenticationService.login(user.email, user.password).then(function (res) {
            if (res) {
                $modalInstance.close(res);
            } else {
                $scope.authError = 'Authentication failure';
            }
        }, function (res) {
            $scope.authError = 'Authentication failure';
        });
    };
    
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);