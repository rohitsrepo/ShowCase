var showcaseApp = angular.module('controller.reader', ['security.service', 'artifact.composition', 'helper.logger']);

showcaseApp.controller('readerCtrl', function ($scope, securityFactory, compositionFactory, logger) {
    'use strict';
    
    $scope.compositions = compositionFactory.manager.query();
    
    $scope.voting = function (index, vote) {
        compositionFactory.votes.put($scope.compositions[index].id, vote).then(function (res) {
            $scope.compositions[index].vote = res.data;
        }, function (res) {
            //TODO handle error according to status of error.
            // Global exception handling.
            logger('Reader controller...error while putting votes', res);
            if (res.status === 403) {
                alert('Seems like you have already voted mate!!!');
            }
        });
    };
});