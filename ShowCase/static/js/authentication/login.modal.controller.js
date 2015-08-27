angular.module('module.auth')
.controller("loginModalController", ["$scope", '$location', '$interval','$cookies', '$window', 'auth', 'close', 'progress', 'alert',
    function ($scope, $location, $interval, $cookies, $window, auth, close, progress, alert) {
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
					close("LoggedIn");
				}, function () {})
			}
			
			if ($cookies.userLoggedIn == provider){
				loopCleaner();
				loginWindow.close();
				close("LoggedIn");
			}

			if ($cookies.userLoggedNot == provider){
				loopCleaner();
				loginWindow.close();
			}
		}
	};

	$scope.socialLogger = function (provider) {
		if (loggingIn) {
			return;
		}


		var loggingIn = true;
		$cookies.userLoggedIn = '';
		$cookies.userLoggedNot = '';

		var url = '/users/login/' + provider + '/'
		var loginWindow = $window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=400,width=600');

		var checkLoginLoop = $interval(loginSocial(clearLoginLoop, loginWindow, provider), 1000);

		function clearLoginLoop () {
			$interval.cancel(checkLoginLoop);
			$cookies.userLoggedIn = '';
			$cookies.userLoggedNot = '';
			loggingIn = false;
		};
	};
}]);