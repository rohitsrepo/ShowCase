var bookmarkModule = angular.module('artifact.bookmark', ['ngResource', 'authentication']);

bookmarkModule.factory('bookmarkFactory', ['$http', '$log', 'authenticationService', '$q',  function ($http, $log, authenticationService, $q) {
    'use strict';
    
    var service = {};
    service.getBookmark = function (userId) {
        return $http({method: 'GET', url: 'users/' + userId + '/bookmarks'}).then(function (res) {
            $log.info(res.data.bookmarks);
            return res.data.bookmarks;
        }, function (res) {
            $log.error('bookmarkFactory: ', res);
        });
    };
    
    service.addBookmark = function (userId, compositionId) {
        if (authenticationService.checkForAuth()) {
            return $http({method: 'POST', data: {bookmarks: [compositionId]}, url: 'users/' + userId + '/bookmarks'}).then(function (res) {
                return res;
            }, function (res) {
                $log.error('bookmarkFactory', res);
            });
        }
        
        return $q.when(false);
    };
    
    service.deleteBookmark = function (userId, compositionId) {
        return $http({method: 'DELETE', data: {bookmarks: [compositionId]}, url: 'users/' + userId + '/bookmarks'}).then(function (res) {
        }, function (res) {
            $log.error('bookmarkFactory', res);
        });
    };
    return service;
}]);