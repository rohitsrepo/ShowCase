angular.module("module.curtainRight")
.controller('rightCurtainController', ['$scope', "auth", "$location", "progress", "alert", function ($scope, auth, $location, progress, alert) {
	'use strict';

	$scope.login = function (user) {
		progress.showProgress();

		auth.login(user.email, user.password, $location.absUrl()).then(function () {
			progress.hideProgress();
		}, function (error) {
			progress.hideProgress();
			alert.showAlert(error);
		});
	};

}]);