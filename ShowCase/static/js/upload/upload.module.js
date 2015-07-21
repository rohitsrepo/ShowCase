angular.module("UploadApp", [
	"module.auth",
	"module.curtainRight",
	"module.curtainLeft",
	"module.topbar",
	"module.scrollTo",
	"module.titlecase",
	"lr.upload",
	"ngAnimate",
	'angucomplete-alt',
    'module.util'])
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
	}, function () {
		$window.location.href="/login#?next=" + $window.location.pathname;
	});
}]);