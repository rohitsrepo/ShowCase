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
			$log.error("Error fetching user list.", response);
		});
	};
	return service;
}]);