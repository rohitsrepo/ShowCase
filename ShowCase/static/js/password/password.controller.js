angular.module("PasswordApp")
.controller("passwordController", ["$scope", "userModel", 'progress', 'alert', function ($scope, userModel, progress, alert)
 {
	"use strict";
	var id, token;

	$scope.init = function (page_type, id, token) {

		$scope.pageType = 1;

		if (page_type == 'reset_password_confirm') {
			$scope.pageType = 2;
			$scope.id = id;
			$scope.token = token;
		} else if (page_type == 'reset_password_confirm_error') {
			$scope.pageType = 3;
		}

	};

	$scope.resetPassword = function (email) {
		progress.showProgress();

		userModel.resetPassword(email).then(function () {
			progress.hideProgress();
			$scope.sendingMail = true;
		}, function () {
			progress.hideProgress();
			alert.showAlert("Unable to create request to reset password")
		})
	};

	$scope.setNewPassword = function (password) {
		progress.showProgress();

		userModel.setNewPassword(password, $scope.id, $scope.token).then(function () {
			progress.hideProgress();
			$scope.passwordChanged = true;
		}, function () {
			progress.hideProgress();
			alert.showAlert("Unable to reset password")
		})
	};

}]);