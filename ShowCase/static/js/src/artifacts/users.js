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
    
    service.addUser = function (user) {
        return $http({method: 'POST', url: '/users', data: user}).then(function (res) {
            return res;
        }, function (res) {
            $log.error('Adding new user: ', res);
        });
    };
    
    service.login = function (email, password) {
        return $http({method: 'POST',
                      url: '/users/login',
                      data: {email: email, password: password}
                     });
    };
    
    service.logout = function () {
        return $http({method: 'GET',
                      url: '/users/logout'
                     });
    };
    
    return service;
}]);