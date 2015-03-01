angular.module("module.model")
.factory('userModel', ['$http', '$log', '$q', function ($http, $log, $q) {
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
			return response;
		})
		.error(function (response, status) {
			return $q.reject(status);
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

	service.getCurrentUser =  function () {
	    return $http.get('/users/currentUser').then(function (response) {
	        return response.data;
	    });
	};

	service.addUser = function (user) {
		return $http.post("/users", user).then(function (response) {
			return response.data;
		}, function (response, status){
			return $q.reject(response);
		})
	};

	return service;
}]);