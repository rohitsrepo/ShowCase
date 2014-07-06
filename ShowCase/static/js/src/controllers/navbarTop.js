var navbarTopModule = angular.module('controller.navbarTop', ['security.service']);

navbarTopModule.controller('navbarTopCtrl', ['$scope', 'securityFactory', '$log', function ($scope, securityFactory, $log) {
    'use strict';
    
    $scope.login = securityFactory.checkForAuth;
    $scope.logout = securityFactory.logout;
}]);