angular.module("model.user", [])
.factory('userModel', ['$http', '$log', function ($http, $log) {
	"use strict";

	var base_url = "/users";
	var service = {};

	service.getList = function () {
		return $http.get(base_url).success(function (response) {
			return response;
		}).error( function (response) {
			$log.error("Error fetching user list.", response);
		});
	};

	service.getUser = function (userId) {
		$http.get(base_url+'/'+userId).success(function (response) {
			return response;
		}).error(function (response) {
			$log.error("Error fetching user: ", response);
		});
	};

	service.login = function (email, password) {
		return $http({method: 'POST', url: '/users/login', data: {email: email, password: password}})
		.success(function (response) {
			$log.info("Logging in user", response);
			return response;
		})
		.error(function (response) {
			$log.error("Error loggin in: ", response);
		});
	};

	service.logout = function () {
		return $http.get('/users/logout')
		.success(function (response) {
			return response;
		})
		.error(function (response) {
			$log.error("Error loggin out: ", response);
		});
	};

	return service;
}]);