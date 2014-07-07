var registerModalModule = angular.module('controller.registerModal', ['ui.bootstrap', 'service.register', 'artifact.user']);

registerModalModule.controller('registerModalCtrl', ['$scope', '$modalInstance', 'registerFactory', 'userFactory', function ($scope, $modalInstance, registerFactory, userFactory) {
    'use strict';
    
    $scope.regError = '';
    
    $scope.register = function (user) {
        $scope.regError = '';
        userFactory.addUser(user).then(function (res) {
            if (res) {
                $modalInstance.close({response: res, user: user});
            } else {
                $scope.regError = 'Registration failure';
            }
        }, function (res) {
            $scope.regError = 'Registration failure';
        });
    };
    
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);