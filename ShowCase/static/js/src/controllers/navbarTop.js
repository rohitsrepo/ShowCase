var navbarTopModule = angular.module('controller.navbarTop', ['authentication', 'register', 'artifact.notification']);

navbarTopModule.controller('navbarTopCtrl', ['$scope', 'authenticationService', 'registerService', 'notificationFactory', function ($scope, authenticationService, registerService, notificationFactory) {
    'use strict';
    
    $scope.login = authenticationService.checkForAuth;
    $scope.logout = authenticationService.logout;
    
    $scope.register = registerService.showRegisterModal;
    
    $scope.$watch(function () {
        return notificationFactory.newNotification;
    }, function (val) {
        $scope.newNotification = val;
    });
}]);