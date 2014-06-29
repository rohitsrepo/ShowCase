var bookmarkModule = angular.module('artifact.bookmark', ['ngResource']);

bookmarkModule.factory('bookmarkFactory', ['$http', '$log', function ($http, $log) {
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
        return $http({method: 'PUT', data: {bookmarks: [compositionId]}, url: 'users/' + userId + '/bookmarks'}).then(function (res) {
            $log.info(res);
        }, function (res) {
            $log.error('bookmarkFactory', res);
        });
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