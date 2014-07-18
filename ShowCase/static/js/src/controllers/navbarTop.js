var navbarTopModule = angular.module('controller.navbarTop', ['security.service', 'service.register', 'artifact.notification']);

navbarTopModule.controller('navbarTopCtrl', ['$scope', 'securityFactory', 'registerFactory', 'notificationFactory', function ($scope, securityFactory, registerFactory, notificationFactory) {
    'use strict';
    
    $scope.login = securityFactory.checkForAuth;
    $scope.logout = securityFactory.logout;
    
    $scope.register = registerFactory.showRegisterModal;
    
    $scope.$watch(function () {
        return notificationFactory.newNotification;
    }, function (val) {
        $scope.newNotification = val;
    });
}]);