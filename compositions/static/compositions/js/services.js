var compositionService = angular.module('compositionService', ['ngResource']);

/*compositionSerivce.factory('compositions', function ($resource) {
    return $resource('compositions/:compositionId.json');
});*/

compositionService.config(function ($httpProvider) {
    /* csrf */
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
});

compositionService.factory('Compositions', function ($resource, $http) {
    var serviceObject = {};
    serviceObject.manager = $resource('/compositions/:compositionID.json', {compositionID: '@id'});
    
    serviceObject.votes = {};
    serviceObject.votes.put = function (compositionId, vote) {
        var votingUrl = '/compositions/' + compositionId + '/vote';
        return $http({method: 'PUT', data: {'vote': vote}, url: votingUrl});
    };
    
    serviceObject.votes.get = function (compositionId){
        var votingUrl = '/compositions/' + compositionId + '/vote';
        return $http({method: 'GET', url: votingUrl});
    };
    
    serviceObject.comments = $resource('/compositions/:compositionId/comments.json');
    
    return serviceObject;
});

