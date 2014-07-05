var rootModule = angular.module('controller.root', ['security.service']);

rootModule.controller('rootCtrl', ['$scope', 'securityFactory', function ($scope, securityFactory) {
    'use strict';
    
    $scope.$watch(function () {
        return securityFactory.currentUser;
    }, function (user) {
        $scope.currentUser = user;
    });
}]);