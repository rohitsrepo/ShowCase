var navbarTopModule = angular.module('controller.navbarTop', ['security.service', 'register', 'artifact.notification']);

navbarTopModule.controller('navbarTopCtrl', ['$scope', 'securityFactory', 'registerService', 'notificationFactory', function ($scope, securityFactory, registerService, notificationFactory) {
    'use strict';
    
    $scope.login = securityFactory.checkForAuth;
    $scope.logout = securityFactory.logout;
    
    $scope.register = registerService.showRegisterModal;
    
    $scope.$watch(function () {
        return notificationFactory.newNotification;
    }, function (val) {
        $scope.newNotification = val;
    });
}]);