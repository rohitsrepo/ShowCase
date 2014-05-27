var navbarTopModule = angular.module('controller.navbarTop', ['security.service']);

navbarTopModule.controller('navbarTopCtrl', ['$scope', 'securityFactory', function ($scope, securityFactory) {
    'use strict';
    
    $scope.currentUser = securityFactory.currentUser;
}]);