angular.module('module.auth')
.controller("loginModalController", ["$scope", '$location', '$interval', '$window', 'auth', 'close', 'progress', 'alert',
    function ($scope, $location, $interval, $window, auth, close, progress, alert) {
	"use strict";

    $scope.showNative = false;
    $scope.showNativeLogin = true;

	$scope.closeModal = function () {
		close();
	}

    $scope.toNative = function () {
        $scope.showNative = true;
        $scope.showNativeLogin = true;
    };

    $scope.toSocial = function () {
        $scope.showNative = false;
    };

    $scope.toNativeLogin = function () {
        $scope.showNativeLogin = true;
    };

    $scope.toNativeCreate = function () {
        $scope.showNativeLogin = false;
    };

	$scope.login = function (user) {
		progress.showProgress();

		auth.loginRaw(user.email, user.password).then(function () {
			progress.hideProgress();
			close("LoggedIn");
		}, function (error) {
			progress.hideProgress();
			alert.showAlert(error);
		});
	};

	$scope.register = function (user) {
		progress.showProgress();

		auth.registerUserRaw(user).then(function () {
			progress.hideProgress();
			close("LoggedIn");
		}, function (error) {
			progress.hideProgress();
			alert.showAlert(error);
		});
	};

	var loginSocial = function (loopCleaner, loginWindow, provider) {
		return function () {
			if (loginWindow.closed) {
				loopCleaner();

				auth.getCurrentUser().then(function (user) {
                    alert.showAlert("Welcome " + user.name);
					close("LoggedIn");
				}, function () {})
			}
		}
	};

	$scope.socialLogger = function (provider) {
		if (loggingIn) {
			return;
		}


		var loggingIn = true;

		var url = '/users/login/' + provider + '/'
		var loginWindow = $window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600');

		var checkLoginLoop = $interval(loginSocial(clearLoginLoop, loginWindow, provider), 1000);

		function clearLoginLoop () {
			$interval.cancel(checkLoginLoop);
			loggingIn = false;
		};
	};
}]);