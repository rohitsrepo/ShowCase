angular.module("RegisterApp")
.controller("registerController", ["$scope", "auth", function ($scope, auth) {
	"use strict";

	$scope.register = function (user) {
		auth.registerUser(user);
	};
}]);