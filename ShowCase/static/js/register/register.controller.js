angular.module("RegisterApp")
.controller("registerController", ["$scope", "auth", 'facebook', function ($scope, auth, facebook) {
	"use strict";

	$scope.hideSignUp = true;

	$scope.register = function (user) {
		user.login_type = "NT"
		auth.registerUser(user);
	};

	$scope.loginFB = function () {
		facebook.login('/');
	}
}]);