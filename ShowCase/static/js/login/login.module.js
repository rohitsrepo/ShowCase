angular.module("LoginApp", ['module.root'])
.config(['$httpProvider', '$interpolateProvider', '$locationProvider', function ($httpProvider, $interpolateProvider, $locationProvider) {
	"use strict";

	// Changing angular template tag to prevent conflict with django
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')

	// csrf for django
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';

	$locationProvider.html5Mode(true);
}]).run(['auth', "$window", function (auth, $window) {
	auth.getCurrentUser().then(function () {
		$window.location.href="/";
	});
}]);