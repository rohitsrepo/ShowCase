angular.module("module.curtainRight")
.controller('rightCurtainController', ['$scope',
    "$location",
    "$window",
    "$interval",
    "auth",
    "progress",
    "alert",
    function ($scope, $location, $window, $interval, auth, progress, alert) {
	'use strict';

	$scope.login = function (user) {
		progress.showProgress();

		auth.login(user.email, user.password, $location.absUrl()).then(function () {
			progress.hideProgress();
            $window.location.reload();
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
                    $window.location.reload();
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