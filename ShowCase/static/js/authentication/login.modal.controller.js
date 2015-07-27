angular.module('module.auth')
.controller("loginModalController", ["$scope", '$location', 'close', 'progress', 'alert', function ($scope, $location, close, progress, alert) {
	"use strict";

	$scope.showNative = false;

	$scope.closeModal = function () {
		close();
	}

	$scope.toggleLoginType = function () {
		$scope.showNative = !$scope.showNative;
	};

	$scope.login = function (user) {
		progress.showProgress();

		auth.login(user.email, user.password, $location.absUrl()).then(function () {
			progress.hideProgress();
		}, function (error) {
			progress.hideProgress();
			alert.showAlert(error);
		});
	};

	$scope.register = function (user) {
		progress.showProgress();

		auth.registerUser(user, $location.absUrl()).then(function () {
			progress.hideProgress();
		}, function (error) {
			progress.hideProgress();
			alert.showAlert(error);
		});
	};

}]);