angular.module('module.auth')
.factory('auth', ['userModel', '$window', '$q', function (userModel, $window, $q) {

	var isAuthenticated = function () {
		return !!service.currentUser;
	};

	var redirect = function (url) {
		console.log("Redirecting to url:", url);
		if(!url)
		{
			$window.location.reload();
		} else {
			console.log("current location", $window.location.href);
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
				error = "This account has been disabeled";
			} else if (response.status==409) {
				error = "This account is not registered with ThirdDime";
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
			userModel.login(user.email, user.password, user.login_type).then(function (res) {
				redirect(next_url || '/');
			}, function (res) {
			});	
		}, function (response) {
			if (response.status === 400) {
				return $q.reject(response.data);
			}
		});
	};

	return service;
}]);