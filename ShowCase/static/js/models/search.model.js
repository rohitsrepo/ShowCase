angular.module("module.model")
.factory('searchModel', ['$http', '$log', '$q', function ($http, $log, $q) {
	"use strict";

	var service = {};

	service.search = function (query) {
		return $http.get('/search?q=' + query).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
	};

	return service;
}]);