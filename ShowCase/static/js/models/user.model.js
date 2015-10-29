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
	    }, function (response) {
            return $q.reject(response);
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

    service.resetNsfw = function (nsfw) {
        return $http.post("/users/reset-nsfw", {'nsfw': nsfw}).then(function (response) {
            return response.data;
        }, function (response, status){
            return $q.reject(response);
        })
    };

    service.getMailOptions = function () {
        return $http.get("/users/mail-options").then(function (response) {
            return response.data;
        }, function (response, status){
            return $q.reject(response);
        })
    };

    service.resetMailOptions = function (mailOptions) {
        return $http.put("/users/mail-options", mailOptions).then(function (response) {
            return response.data;
        }, function (response, status){
            return $q.reject(response);
        })
    };

    service.resetPicture = function (profilePictureData) {
        return $http.post('/users/reset-picture', profilePictureData).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

	service.getCompositions = function (user_id, page) {
		return $http.get('/users/'+user_id+'/compositions?page='+page).then(function (response) {
			return response.data;
		}, function (response) {
            return $q.reject(response);
        });
	};

    service.getUploads = function (user_id, page) {
        return $http.get('/users/'+user_id+'/uploads?page='+page).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.follow = function (user_id) {
    	return $http.post('/users/follows', {'follows': [user_id]}).then(function (response) {
    		return response.data;
    	}, function (response) {
    		return $q.reject(response);
    	});
    };

    service.unfollow = function (user_id) {
    	return $http.delete('/users/follows/'+user_id).then(function (response) {
    		return response.data;
    	}, function (response) {
    		return $q.reject(response);
    	});
    };

    service.getFollowers = function (user_id) {
        return $http.get('/users/'+user_id+'/followers').then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.getFollows = function (user_id) {
        return $http.get('/users/'+user_id+'/follows').then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.resetPassword = function (email) {
        return $http.post('/users/reset-password', {'email': email}).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.setNewPassword = function (password, id, token) {
        return $http.post('/users/reset-password-confirm/' + id + '-' + token, {'password': password}).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

	return service;
}]);