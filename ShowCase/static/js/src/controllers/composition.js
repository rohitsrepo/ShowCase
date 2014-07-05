var compositionCtrlModule = angular.module('controller.composition', ['security.service', 'artifact.composition', 'ui.router', 'artifact.bookmark']);

compositionCtrlModule.controller('compositionCtrl', ['$scope',
                                                    'securityFactory',
                                                    'compositionFactory',
                                                    '$stateParams',
                                                    '$location',
                                                    '$window',
                                                    '$log',
                                                    'bookmarkFactory', function ($scope, securityFactory, compositionFactory, $stateParams, $location, $window, $log, bookmarkFactory) {
    'use strict';
    $scope.$watch(function () {
        return securityFactory.currentUser;
    }, function (user) {
        $scope.currentUser = user;
    });
    
    $scope.newComment = '';
    $scope.isAuthenticated = securityFactory.isAuthenticated;
    
    $scope.composition = compositionFactory.manager.get({compositionId: $stateParams.compositionId}, function (data) {
        if ((data.slug).localeCompare($stateParams.slug)) {
            $location.path('compositions/' + data.id + '/' + data.slug);
        }
        $scope.comments = compositionFactory.comments.query({compositionId: $stateParams.compositionId});
    });
    
    $scope.voting = function (vote) {
        compositionFactory.votes.put($scope.composition.id, vote).then(function (res) {
            if (res) {
                $scope.composition.vote = res.data;
                $scope.composition.IsVoted = true;
            }
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
        securityFactory.checkForAuth();
        var res = compositionFactory.comments.save({compositionId: $scope.composition.id}, {comment: $scope.newComment}, function (res) {
            $scope.comments.push(res);
            $scope.newComment = '';
        });
    };
    
    $scope.isCompositionOwner = compositionFactory.isOwner;
    
    $scope.editComposition = function () {
        console.log($scope.composition);
        compositionFactory.manager.update({compositionId: $scope.composition.id},
                                          {title: $scope.composition.title, description: $scope.composition.description},
                                          function (data) {
                                              alert('Successfully updated composition.');
                                              //TODO - update this logic - page upload should not be required.
                                              $window.location.reload();
                                          });
    };
    
    $scope.removeComposition = function () {
        $scope.composition.$delete(function () {
            alert('Successfully deleted composition :( ');
            //TODO may be back to the last page instead of home page.
            $window.location.href = '#/popular';
        });
    };
                                                        
    $scope.bookmark = function (compositionId) {
        if (securityFactory.checkForAuth()) {
            bookmarkFactory.addBookmark($scope.currentUser.id, compositionId).then(function (res) {
                $log.info('got in return', res);
                if (res) {
                    $scope.composition.IsBookmarked = true;
                } else {
                    $log.info('Seems like auth reluctance by user.');
                };
            }, function (res) {});
        }
    };
}]);