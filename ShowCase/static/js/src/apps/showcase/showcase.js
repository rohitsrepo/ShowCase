var showcaseModule = angular.module('showcase.module', ['artifact.composition', 'authentication', 'artifact.follow']);

showcaseModule.controller('showcaseController', ['$scope', 'compositionFactory', 'getUser', 'authenticationService', '$log', 'followFactory', function ($scope, compositionFactory, getUser, authenticationService, $log, followFactory) {
    'use strict';
    
    $scope.user = getUser;
    $scope.compositions = compositionFactory.manager.query({artist: $scope.user.id});
    
    $scope.follow = function () {
        if (authenticationService.checkForAuth()) {
            followFactory.follow($scope.currentUser.id, $scope.user.id).then(function (res) {
                $scope.user.IsFollowed = true;
            }, function (res) {
                $log.error('Follow this user: ', res);
            });
        }
    };
    
    $scope.unFollow = function () {
        if (authenticationService.checkForAuth()) {
            followFactory.unFollow($scope.currentUser.id, $scope.user.id).then(function (res) {
                $scope.user.IsFollowed = false;
            }, function (res) {
                $log.error('Un-Follow this user: ', res);
            });
        }
    };
}]);