angular.module('module.auth', ['model.user'])
.factory('auth', ['userModel', '$window', '$q', function (userModel, $window, $q) {

	var isAuthenticated = function () {
		return !!service.currentUser;
	};

	var redirect = function () {
		$window.location.reload();
	};

	var service = {};
	service.login = function (email, password) {
		return userModel.login(email, password).then(function (user) {
			currentUser = user;
			redirect();
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

	return service;
}]);