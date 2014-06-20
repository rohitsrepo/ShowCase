var compositionServiceModule = angular.module('artifact.composition', ['ngResource', 'security.service']);

compositionServiceModule.factory('compositionFactory', ['$resource', '$http', 'securityFactory', function ($resource, $http, securityFactory) {
    'use strict';
    
    var service = {};
    service.manager = $resource('/compositions/:compositionId.json', {compositionId: '@id'}, 
                                {
                                    'update': { method: 'PUT'}
                                });
    
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
    
    service.isOwner = function (userId) {
        return userId === securityFactory.currentUser.id;
    };
    
    return service;
}]);

