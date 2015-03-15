angular.module("RegisterApp")
.controller("registerController", ["$scope", "auth", function ($scope, auth) {
	"use strict";

	$scope.hideSignUp = true;

	$scope.register = function (user) {
		auth.registerUser(user);
	};
}]);