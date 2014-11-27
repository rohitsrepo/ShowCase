angular.module('showcaseApp')
.controller('rootController', ['$scope', 'authenticationService', function ($scope, authenticationService) {
    'use strict';
    
    $scope.$watch(function () {
        return authenticationService.currentUser;
    }, function (user) {
        $scope.currentUser = user;
    });
}]);