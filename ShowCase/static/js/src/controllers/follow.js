var followModule = angular.module('controller.follow', ['artifact.follow']);

followModule.controller('followCtrl', ['$scope', 'followFactory', '$log', 'getUser', function ($scope, followFactory, $log, getUser) {
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