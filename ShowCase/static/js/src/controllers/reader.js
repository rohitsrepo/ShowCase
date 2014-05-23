var showcaseApp = angular.module('controller.reader', ['security.service', 'artifact.composition', 'helper.logger']);

showcaseApp.controller('readerCtrl', function ($scope, securityFactory, compositionFactory, logger) {
    'use strict';
    
    securityFactory.getCurrentUser().then(function (user) {
        $scope.currentUser = user;
    });
    
    $scope.compositions = compositionFactory.manager.query(function (data) {
        angular.forEach(data, function (composition, key) {
            compositionFactory.votes.get(composition.id).then(function (vote) {
                $scope.compositions[key].vote = vote;
            });
        });
    });
    
    $scope.voting = function (composition, vote) {
        compositionFactory.votes.put(composition.id, vote).then(function (res) {
            $scope.vote = res.data;
        }, function (res) {
            //TODO handle error according to status of error.
            // Global exception handling.
            logger('Reader controller...error while putting votes', res);
        });
    };
});