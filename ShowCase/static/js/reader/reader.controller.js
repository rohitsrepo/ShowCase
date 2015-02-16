angular.module("ReaderApp")
.controller("readerController", ["$scope", "userModel", function ($scope, userModel) {
	"use strict";

	$scope.loginUser = function (user) {
		userModel.login(user.email, user.password);
	};
}]);