var compositionServiceModule = angular.module('artifact.composition', ['ngResource', 'authentication']);

compositionServiceModule.factory('compositionFactory', ['$resource', '$http', 'authenticationService', '$q', function ($resource, $http, authenticationService, $q) {
    'use strict';
    
    var service = {};
    service.manager = $resource('/compositions/:compositionId.json', {compositionId: '@id'},
                                {
                                    'update': { method: 'PUT'}
                                });
    
    service.votes = {};
    service.votes.put = function (compositionId, vote) {
        if (authenticationService.checkForAuth()) {
            var votingUrl = '/compositions/' + compositionId + '/vote';
            return $http({method: 'PUT', data: {'vote': vote}, url: votingUrl});
        }
        return $q.when(false);
    };
    
    service.votes.get = function (compositionId) {
        var votingUrl = '/compositions/' + compositionId + '/vote';
        return $http({method: 'GET', url: votingUrl}).then(function (res) {
            return res.data;
        }, function (res) {
            //TODO handle all the errors here. Ideally they should not be propagated further
            // as per current design/.
            return res;
        });
    };
    
    service.comments = $resource('/compositions/:compositionId/comments.json');
    
    service.isOwner = function (userId) {
        return userId === (authenticationService.currentUser && authenticationService.currentUser.id);
    };
    
    return service;
}]);

