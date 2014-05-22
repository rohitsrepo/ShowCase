var showcaseApp = angular.module('controller.reader', ['security.service', 'artifact.composition', 'helper.logger']);

showcaseApp.controller('readerCtrl', function ($scope, securityFactory, compositionFactory, logger) {
    'use strict';
    
    $scope.newComment = '';
    
    $scope.currentUser = securityFactory.getCurrentUser().then(function (user) {
        $scope.currentUser = user;
    });
    
    $scope.compositions = compositionFactory.manager.query(function (data) {
        $scope.showComposition($scope.compositions[0]);
    });
    
    $scope.showComposition = function (composition) {
        $scope.currentComposition = composition;
        compositionFactory.votes.get(composition.id).then(function (res) {
            $scope.vote = res.data;
        }, function (res) {
            //TODO handle error according to status of error.
            // Global exception handling.
            logger('Reader controller....while getting votes', res);
        });
        
        $scope.comments = compositionFactory.comments.query({compositionId: composition.id});
    };
    
    $scope.isActive = function (compositionId) {
        return compositionId === $scope.currentComposition.id;
    };
    
    $scope.deleteComposition = function (composition) {
        compositionFactory.manager.delete({compositionId: $scope.currentComposition.id});
    };
    
    $scope.voting = function (vote) {
        compositionFactory.votes.put($scope.currentComposition.id, vote).then(function (res) {
            $scope.vote = res.data;
        }, function (res) {
            //TODO handle error according to status of error.
            // Global exception handling.
            logger('Reader controller...error while putting votes', res);
        });
    };
    
    $scope.commenting = function () {
        var res = compositionFactory.comments.save({compositionId: $scope.currentComposition.id}, {comment: $scope.newComment}, function (res) {
            $scope.comments = compositionFactory.comments.query({compositionId: $scope.currentComposition.id});
            $scope.newComment = '';
        });
        
    };
});