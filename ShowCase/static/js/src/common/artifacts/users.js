var userModule = angular.module('artifact.user', ['ngResource']);

userModule.factory('userFactory', [ '$http', '$resource', '$log', function ($http, $resource, $log) {
    'use strict';
    
    var service = {};
    
    service.getCurrentUser =  function () {
        return $http({method: 'GET', url: 'users/currentUser.json'}).then(function (res) {
            return res.data;
        }, function (res) {
            //TODO: remove console logging and may be do something to contain the failure.
            $log.error('Trying to user in session: ', res);
        });
    };
    
    service.getUser = function (userId) {
        var url = '/users/' + userId;
        return $http({method: 'GET', url: url});
    };
    
    return service;
}]);