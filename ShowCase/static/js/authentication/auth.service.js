angular.module('module.auth')
.factory('auth', ['userModel', '$window', '$q', function (userModel, $window, $q) {

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
		return userModel.login(email, password).then(function (user) {
			currentUser = user;
			var next_url = nextUrl || "/"
			redirect(next_url);
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
			return $q.when(service.currentUser);
		} else {
			return userModel.getCurrentUser().then(function (user) {
				service.currentUser = user;
				return service.currentUser;
			});
		}
	};

	service.registerUser = function (user, next_url) {
		return userModel.addUser(user).then(function (response){
			redirect(next_url || '/');
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

	return service;
}]);