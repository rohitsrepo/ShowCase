var compositionServiceModule = angular.module('artifact.composition', ['ngResource']);

compositionServiceModule.factory('compositionFactory', function ($resource, $http) {
    'use strict';
    
    var service = {};
    service.manager = $resource('/compositions/:compositionId.json', {compositionId: '@id'});
    
    service.votes = {};
    service.votes.put = function (compositionId, vote) {
        var votingUrl = '/compositions/' + compositionId + '/vote';
        return $http({method: 'PUT', data: {'vote': vote}, url: votingUrl});
    };
    
    service.votes.get = function (compositionId) {
        var votingUrl = '/compositions/' + compositionId + '/vote';
        return $http({method: 'GET', url: votingUrl}).then(function (res) {
            return res.data;
        }, function (res) {
            //TODO handle all the errors here. Ideally they should not be propagated further
            // as per surrent design/.
            return res;
        });
    };
    
    service.comments = $resource('/compositions/:compositionId/comments.json');
    
    return service;
});

