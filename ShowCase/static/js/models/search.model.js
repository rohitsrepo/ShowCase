angular.module("module.model")
.factory('searchModel', ['$http', '$log', '$q', function ($http, $log, $q) {
	"use strict";

	var service = {};

    service.search = function (query, page) {
        return $http.get('/api/search?q=' + query + '&page=' + page).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.searchUsers = function (query, page) {
        return $http.get('/api/search/users?q=' + query + '&page=' + page).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.searchBuckets = function (query, page) {
        return $http.get('/api/search/buckets?q=' + query + '&page=' + page).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.searchArts = function (query, page) {
        return $http.get('/api/search/compositions?q=' + query + '&page=' + page).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

	return service;
}]);