angular.module('module.auth')
.factory('auth', ['userModel', '$window', '$q', '$rootScope', 'modalService', function (userModel, $window, $q, $rootScope, modalService) {

	var isAuthenticated = function () {
		return !!service.currentUser;
	};

	var redirect = function (url) {
		if(!url)
		{
			$window.location.reload();
		} else {
			if (url === $window.location.href){
				$window.location.reload();
			}
			$window.location.href = url;
		}
	};

	var service = {};
	service.login = function (email, password, nextUrl) {
		return service.loginRaw(email, password).then(function () {
			var next_url = nextUrl || "/"
			redirect(next_url);
		}, function (error) {
			return $q.reject(error);
		});
	}

	service.loginRaw = function (email, password) {
		return userModel.login(email, password).then(function (user) {
			currentUser = user;
			$rootScope.userIsNowLoggedIn = true;
			return $q.when(user);
		}, function (response) {
			var error;
			if (response.status==401){
				error = "Username and Password did not match";
			} else if (response.status==402) {
				error = "This account has been disabled";
			} else if (response.status==409) {
				error = "This account is not registered with ThirdDime";
			} else if (response.status==406) {
				error = "Please login using social media.";
			} else {
				error = "Could not contact server";
			}
			return $q.reject(error);
		});
	}

	service.logout = function () {
		userModel.logout().then(function () {
			currentUser = null;
			redirect();
		})
	};

	service.getCurrentUser = function () {
		if (isAuthenticated()){
			$rootScope.userIsNowLoggedIn = true;
			return $q.when(service.currentUser);
		} else {
			return userModel.getCurrentUser().then(function (user) {
				service.currentUser = user;
				$rootScope.userIsNowLoggedIn = true;
				return service.currentUser;
			}, function () {
				return $q.reject();
			});
		}
	};

	service.registerUser = function (user, next_url) {
		return service.registerUserRaw(user).then(function(user){
			redirect(next_url || '/');
		}, function (error) {
			return $q.reject(error);
		});
	};

	service.registerUserRaw = function (user) {
		return userModel.addUser(user).then(function (user){
			currentUser = user;
			$rootScope.userIsNowLoggedIn = true;
			return $q.when(user);
		}, function (response) {
			if (response.status === 400) {
				return $q.reject("We are unable to process this request. Please check the information you have provided.");
			} else if (response.status == 402) {
				return $q.reject("This account is not active. Please contact Thirddime team directly.");
			} else if (response.status == 409) {
				return $q.reject("This account is registered using social media. Please login using the same.");
			} else{
				return $q.reject("We are unable to process this request. Please try again later.");
			}
		});
	};

	var showLoginModal = function () {

		return modalService.showModal({
			'templateUrl': '/static/js/authentication/login.tpl.html',
			'controller': 'loginModalController'
		});
	};

	service.runWithAuth = function (callback) {

		return service.getCurrentUser().then(function (user) {
			if (typeof callback == 'function') {
				return callback(user);
			}
		}, function () {
			return showLoginModal().then(function (modal) {
				return modal.close.then(function (response) {
					if (response == "LoggedIn") {
						service.getCurrentUser().then(function (user) {
							if (typeof callback == 'function') {
	                            callback(user);
	                        }
                            
                            redirect();
                        });   // call to make sure auth service has the new user
					} else {
						if (typeof callback == 'function') {
                            return $q.reject(callback());
                        }
					}
				});
			});

		})
	};

	return service;
}]);