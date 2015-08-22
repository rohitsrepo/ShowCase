angular.module("LoginApp")
.controller("loginController", ["$scope", "auth", '$location', "progress", "alert", function ($scope, auth, $location, progress, alert) {
	"use strict";

    var next = '/';
    $scope.init = function () {
    	if ($location.search()) {
	        next = $location.search()['next'] || next;
    	}
        console.log('next', next);
    };
    $scope.init();

	$scope.login = function (user) {
		progress.showProgress();

		auth.login(user.email, user.password, next).then(function () {
			progress.hideProgress();
		}, function (error) {
			progress.hideProgress();
			alert.showAlert(error);
		});
	};
}]);