var compositionCtrlModule = angular.module('controller.composition', ['security.service', 'artifact.composition', 'ui.router']);

compositionCtrlModule.controller('compositionCtrl',['$scope', 'securityFactory', 'compositionFactory', '$stateParams', '$location', '$window', function ($scope, securityFactory, compositionFactory, $stateParams, $location, $window) {
    'use strict';
    
    $scope.newComment = '';
    
    $scope.composition = compositionFactory.manager.get({compositionId: $stateParams.compositionId}, function (data) {
        if ((data.slug).localeCompare($stateParams.slug)) {
            $location.path('compositions/' + data.id + '/' + data.slug);
        }
        $scope.comments = compositionFactory.comments.query({compositionId: $stateParams.compositionId});
    });
    
    $scope.voting = function (vote) {
        compositionFactory.votes.put($scope.composition.id, vote).then(function (res) {
            $scope.composition.vote = res.data;
        }, function (res) {
            //TODO handle error according to status of error.
            // Global exception handling.
            console.log('Reader controller...error while putting votes', res);
            if (res.status === 403) {
                alert('Seems like you have already voted mate!!!');
            }
        });
    };
    
    $scope.commenting = function () {
        var res = compositionFactory.comments.save({compositionId: $scope.composition.id}, {comment: $scope.newComment}, function (res) {
            //TODO - instead of reloading all comments - just append the new comment to the list - If control reaches here we already know that the request passed.
            $scope.comments = compositionFactory.comments.query({compositionId: $scope.composition.id});
            $scope.newComment = '';
        });
    };
    
    $scope.isCompositionOwner = compositionFactory.isOwner;
    
    $scope.editComposition = function () {
        console.log($scope.composition);
        compositionFactory.manager.update({compositionId: $scope.composition.id},
                                          {title: $scope.composition.title, description: $scope.composition.description},
                                          function () {
                                              alert('Successfully updated composition.');
                                          });
    };
    
    $scope.removeComposition = function () {
        $scope.composition.$delete(function () {
            alert('Successfully deleted composition :( ');
            //TODO may be back to the last page instead of home page.
            $window.location.href = '#/popular';
        });
    }
}]);