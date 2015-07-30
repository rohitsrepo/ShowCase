angular.module("LoginApp", ['module.root'])
.config(['$httpProvider', '$interpolateProvider', function ($httpProvider, $interpolateProvider) {
	"use strict";

	// Changing angular template tag to prevent conflict with django
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')

	// csrf for django
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]).run(['auth', "$window", function (auth, $window) {
	auth.getCurrentUser().then(function () {
		$window.location.href="/";
	});
}]);