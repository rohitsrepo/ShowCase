angular.module('showcaseApp')
.controller('rootController', ['$scope', 'securityFactory', function ($scope, securityFactory) {
    'use strict';
    
    $scope.$watch(function () {
        return securityFactory.currentUser;
    }, function (user) {
        $scope.currentUser = user;
    });
}]);