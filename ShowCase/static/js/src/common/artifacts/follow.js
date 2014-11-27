var followModule = angular.module('artifact.follow', ['ngResource', 'authentication']);

followModule.factory('followFactory', ['$http', '$q', '$log', 'authenticationService', function ($http, $q, $log, authenticationService) {
    'use strict';
    
    var service = {};
    service.follow = function (currentUserId, userId) {
        if (authenticationService.checkForAuth()) {
            return $http({method: 'PUT', url: '/users/' + currentUserId + '/follows', data: {follows: [userId]}}).then(function (res) {
                $log.info(res);
                return res;
            }, function (res) {
                $log.error('Trying to add user to follow:', res);
            });
        }
        return $q.when(false);
    };
    
    service.unFollow = function (currentUserId, userId) {
        if (authenticationService.checkForAuth()) {
            return $http({method: 'POST', url: '/users/' + currentUserId + '/follows', data: {follows: [userId]}}).then(function (res) {
                $log.info(res);
                return res;
            }, function (res) {
                $log.error('Trying to un-follow:', res);
            });
        }
        return $q.when(false);
    };
    
    service.getFollowCompositions = function (userId) {
        if (authenticationService.checkForAuth()) {
            return $http({method: 'GET', url: '/compositions/follow'}).then(function (res) {
                return res;
            }, function (res) {
                $log.error('Trying to un-follow:', res);
            });
        }
        return $q.when(false);
    };
    
    return service;
}]);