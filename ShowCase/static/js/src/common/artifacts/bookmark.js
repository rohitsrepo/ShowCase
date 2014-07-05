var bookmarkModule = angular.module('artifact.bookmark', ['ngResource', 'security.service']);

bookmarkModule.factory('bookmarkFactory', ['$http', '$log', 'securityFactory', '$q',  function ($http, $log, securityFactory, $q) {
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
        if (securityFactory.checkForAuth()) {
            return $http({method: 'PUT', data: {bookmarks: [compositionId]}, url: 'users/' + userId + '/bookmarks'}).then(function (res) {
                $log.info(res);
                return res;
            }, function (res) {
                $log.error('bookmarkFactory', res);
            });
        }
        
        return $q.when(false);
    };
    
    service.deleteBookmark = function (userId, compositionId) {
        return $http({method: 'POST', data: {bookmarks: [compositionId]}, url: 'users/' + userId + '/bookmarks'}).then(function (res) {
            $log.info(res);
        }, function (res) {
            $log.error('bookmarkFactory', res);
        });
    };
    return service;
}]);