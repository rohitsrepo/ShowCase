var navbarTopModule = angular.module('controller.navbarTop', ['security.service']);

navbarTopModule.controller('navbarTopCtrl', ['$scope', 'securityFactory', '$log', function ($scope, securityFactory, $log) {
    'use strict';
    
    $scope.$watch(function () {
        return securityFactory.currentUser;
    }, function (user) {
        $scope.currentUser = user;
    });
    
    $scope.login = securityFactory.checkForAuth;
    $scope.logout = securityFactory.logout;
}]);