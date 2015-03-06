angular.module("RegisterApp", ["module.auth"])
.config(['$httpProvider', function ($httpProvider) {
	"use strict";

	// csrf for django
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]).run(['auth', "$window", function (auth, $window) {
	auth.getCurrentUser().then(function () {
		$window.location.href="/";
	});
}]);