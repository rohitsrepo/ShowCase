angular.module('module.auth', ['module.model'])
.factory('auth', ['userModel', '$window', '$q', function (userModel, $window, $q) {

	var isAuthenticated = function () {
		return !!service.currentUser;
	};

	var redirect = function (url) {
		if(!url)
		{
			$window.location.reload();
		} else {
			$window.location.href = url;
		}
	};

	var service = {};
	service.login = function (email, password, nextUrl) {
		return userModel.login(email, password).then(function (user) {
			currentUser = user;
			var next_url = next_url || "/"
			redirect(next_url);
			return user;
		}, function (response) {
			var error;
			if (response.status==401){
				error = "UserName or password did not match";
			} else if (response.status==402) {
				error = "This account is disabeled";
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

	service.registerUser = function (user) {
		userModel.addUser(user).then(function (response){
			userModel.login(user.email, user.password).then(function (res) {
				console.log("login says", res);
				redirect('/');
			}, function (res) {
				console.log("Err login says", res);
			});	
		}, function (response) {
			if (response.status === 400) {
				return $q.reject(response.data);
			}
		});
	};

	return service;
}]);