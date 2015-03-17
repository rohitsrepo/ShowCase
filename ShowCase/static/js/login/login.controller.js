angular.module("LoginApp")
.controller("loginController", ["$scope", "auth", function ($scope, auth) {
	"use strict";

	$scope.login = function (user) {
		auth.login(user.email, user.password).then(function () {
			$scope.loginError = '';
		}, function (error) {
			$scope.loginError = error;
		});
	};

	$scope.hideLogin = true;
}]);