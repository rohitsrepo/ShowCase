angular.module("RegisterApp")
.controller("registerController", ["$scope",
	'$location',
	'$window',
	'$interval',
	"auth",
	"progress",
	"alert",
	function ($scope, $location, $window, $interval, auth, progress, alert) {
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

	var loginSocial = function (loopCleaner, loginWindow, provider) {
	    return function () {
	        if (loginWindow.closed) {
	            loopCleaner();

	            auth.getCurrentUser().then(function (user) {
	                $window.location.href = '/home';
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
        var loginWindow = $window.open(url, '_blank', 'menubar=no,toolbar=no,resizable=no,scrollbars=no,height=600,width=600');

        var checkLoginLoop = $interval(loginSocial(clearLoginLoop, loginWindow, provider), 1000);

        function clearLoginLoop () {
            $interval.cancel(checkLoginLoop);
            loggingIn = false;
        };
    }

}]);