angular.module("RegisterApp")
.controller("registerController", ["$scope", "auth", function ($scope, auth) {
	"use strict";

	$scope.hideSignUp = true;

	$scope.register = function (user) {
		user.login_type = "NT"
		auth.registerUser(user);
	};
}]);