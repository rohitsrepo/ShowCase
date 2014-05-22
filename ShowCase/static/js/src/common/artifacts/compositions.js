var compositionServiceModule = angular.module('artifact.composition', ['ngResource']);

/*compositionSerivce.factory('compositions', function ($resource) {
    return $resource('compositions/:compositionId.json');
});*/

/*compositionServiceModule.config(function ($httpProvider) {
    / csrf /
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
});*/

compositionServiceModule.factory('compositionFactory', function ($resource, $http) {
    'use strict';
    
    var service = {};
    service.manager = $resource('/compositions/:compositionID.json', {compositionID: '@id'});
    
    service.votes = {};
    service.votes.put = function (compositionId, vote) {
        var votingUrl = '/compositions/' + compositionId + '/vote';
        return $http({method: 'PUT', data: {'vote': vote}, url: votingUrl});
    };
    
    service.votes.get = function (compositionId) {
        var votingUrl = '/compositions/' + compositionId + '/vote';
        return $http({method: 'GET', url: votingUrl});
    };
    
    service.comments = $resource('/compositions/:compositionId/comments.json');
    
    return service;
});

