var followModule = angular.module('follow.module', ['artifact.follow']);

followModule.controller('followController', ['$scope', 'followFactory', '$log', 'getUser', function ($scope, followFactory, $log, getUser) {
    'use strict';
    
    $scope.user = getUser;
    followFactory.getFollowCompositions($scope.user.id).then(function (res) {
        if (res) {
            $scope.compositions = res.data;
        }
    }, function (res) {
        $log.error('Getting followed compositions: ', res);
    });
}]);