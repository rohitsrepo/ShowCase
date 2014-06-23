var userModule = angular.module('artifact.user', ['ngResource', 'helper.logger']);

userModule.factory('userFactory', function ($http, $resource, logger) {
    'use strict';
    
    var service = {};
    
    service.getCurrentUser =  function () {
        return $http({method: 'GET', url: 'users/currentUser.json'}).then(function (res) {
            return res.data;
        }, function (res) {
            //TODO: remove console logging and may be do something to contain the failure.
            logger('User factory', res);
        });
    };
    service.getUser = function (userId) {
        var url = '/users/' + userId;
        return $http({method: 'GET', url: url});
    };
    
    return service;
});