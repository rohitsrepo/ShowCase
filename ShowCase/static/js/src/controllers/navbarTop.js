var navbarTopModule = angular.module('controller.navbarTop', ['security.service']);

navbarTopModule.controller('navbarTopCtrl', ['$scope', 'securityFactory', function ($scope, securityFactory) {
    'use strict';
    
    $scope.$watch(function () {
        return securityFactory.currentUser;
    }, function (user) {
        $scope.currentUser = user;
    });
    
    $scope.login = securityFactory.showLoginModal;
    $scope.logout = securityFactory.logout;
}]);