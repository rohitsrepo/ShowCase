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

	service.login = function (email, password, login_type) {
		login_type = login_type || "NT";

		return $http({method: 'POST', url: '/users/login', data: {email: email, password: password, login_type: login_type}})
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

    service.resetName = function (name) {
        return $http.post("/users/reset-name", {'name': name}).then(function (response) {
            return response.data;
        }, function (response, status){
            return $q.reject(response);
        })
    };

    service.resetAbout = function (about) {
        return $http.post("/users/reset-about", {'about': about}).then(function (response) {
            return response.data;
        }, function (response, status){
            return $q.reject(response);
        })
    };

	service.getCompositions = function (user_id, page) {
		return $http.get('/users/'+user_id+'/compositions?page='+page).then(function (response) {
			return response.data;
		})
	};

    service.getUploads = function (user_id, page) {
        return $http.get('/users/'+user_id+'/uploads?page='+page).then(function (response) {
            return response.data;
        })
    };

    service.getInterpretations = function (user_id, page) {
        return $http.get('/users/'+user_id+'/interpretations?page='+page).then(function (response) {
            return response.data;
        })
    };

    service.addToCollection = function (art_id) {
    	return $http.post('/users/bookmarks', {'bookmarks': [art_id]}).then(function (response) {
    		return response.data;
    	}, function (response) {
    		$q.reject(response);
    	});
    };

	return service;
}]);