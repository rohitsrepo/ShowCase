angular.module("module.model")
.factory('compositionModel', ['$http', '$log', '$q', function ($http, $log, $q) {
	"use strict";

	var base_url = "/compositions";
	var service = {};

	service.getExplores = function (pageVal) {
		var url = base_url + "/explore" + "?page=" + pageVal;
		return $http.get(url).then(function (response) {
			return response.data;
		},function (response) {
			$log.error("Error fetching art list.", response);
		});
	};

    service.getBookMarkers = function (compositionId) {
        return $http.get('/compositions/' + compositionId + '/bookmarkers').then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.getSerieses = function (compositionId) {
        return $http.get('/compositions/' + compositionId + '/buckets').then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

	return service;
}]);