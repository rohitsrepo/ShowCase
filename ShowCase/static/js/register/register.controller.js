angular.module("RegisterApp")
.controller("registerController", ["$scope", "auth", "progress", "alert", function ($scope, auth, progress, alert) {
	"use strict";

	$scope.hideSignUp = true;

	$scope.register = function (user) {
		progress.showProgress();

		auth.registerUser(user).then(function () {
			progress.hideProgress();
		}, function (error) {
			progress.hideProgress();
			alert.showAlert(error);
		});
	};
}]);