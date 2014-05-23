var compositionCtrlModule = angular.module('controller.composition', ['security.service', 'artifact.composition', 'ui.router']);

compositionCtrlModule.controller('compositionCtrl', function ($scope, securityFactory, compositionFactory, $stateParams) {
    'use strict';
    
    securityFactory.getCurrentUser().then(function (user) {
        $scope.currentUser = user;
    });
    
    $scope.composition = compositionFactory.manager.get({compositionId: $stateParams.compositionId}, function (data) {
        compositionFactory.votes.get($stateParams.compositionId).then(function (votes) {
            $scope.vote = votes;
            $scope.comments = compositionFactory.comments.query({compositionId: $stateParams.compositionId});
        });
    });
});