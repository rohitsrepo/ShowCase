var navbarTopModule = angular.module('controller.navbarTop', ['security.service', 'service.register']);

navbarTopModule.controller('navbarTopCtrl', ['$scope', 'securityFactory', 'registerFactory', function ($scope, securityFactory, registerFactory) {
    'use strict';
    
    $scope.login = securityFactory.checkForAuth;
    $scope.logout = securityFactory.logout;
    
    $scope.register = registerFactory.showRegisterModal;
}]);